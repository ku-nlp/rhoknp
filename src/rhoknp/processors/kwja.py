import logging
import select
import subprocess
import threading
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

try:
    from typing import override  # type: ignore
except ImportError:
    from typing_extensions import override

from rhoknp.processors.processor import Processor
from rhoknp.units import Document, Morpheme, Sentence
from rhoknp.utils.comment import is_comment_line

logger = logging.getLogger(__name__)


class KWJA(Processor):
    """KWJA クラス．

    Args:
        executable: KWJA のパス．
        options: KWJA のオプション．
        skip_sanity_check: True なら，KWJA の起動時に sanity check をスキップする．

    Example:
        >>> from rhoknp import KWJA
        >>> kwja = KWJA()
        >>> document = kwja.apply("電気抵抗率は電気の通しにくさを表す物性値である。")

    .. note::
        使用するには `KWJA <https://github.com/ku-nlp/kwja>`_ がインストールされている必要がある．
    """

    def __init__(
        self,
        executable: str = "kwja",
        options: Optional[List[str]] = None,
        skip_sanity_check: bool = False,
    ) -> None:
        self.executable = executable  #: KWJA のパス．
        self.options: List[str] = options or []  #: KWJA のオプション．
        self._proc: Optional[Popen] = None
        self._lock = Lock()
        self._output_format: str = "knp"
        self._input_format: str = "raw"
        if "--tasks" in self.options:
            tasks: List[str] = self.options[self.options.index("--tasks") + 1].split(",")
            if "word" in tasks:
                self._output_format = "knp"
            elif "seq2seq" in tasks:
                self._output_format = "jumanpp"
            elif "char" in tasks:
                self._output_format = "words"
            elif "typo" in tasks:
                self._output_format = "raw"
            else:
                raise ValueError(f"invalid task: {tasks}")
        # `--input-format` option is available since KWJA v2.2.0
        if "--input-format" in self.options:
            input_format: str = self.options[self.options.index("--input-format") + 1]
            if input_format not in ("raw", "jumanpp", "knp"):
                raise ValueError(f"invalid input format: {input_format}")
            self._input_format = input_format
        self.start_process(skip_sanity_check)

    def __repr__(self) -> str:
        arg_string = f"executable={self.executable!r}"
        if self.options:
            arg_string += f", options={self.options!r}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        if self._proc is not None:
            self._proc.terminate()

    def start_process(self, skip_sanity_check: bool = False) -> None:
        """KWJA を起動する．

        .. note::
            KWJA がすでに起動している場合は再起動する．
            skip_sanity_check: True なら，KWJA の起動時に sanity check をスキップする．
        """
        if self._proc is not None:
            self._proc.terminate()
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
            if skip_sanity_check is False:
                if self._input_format == "raw":
                    empty_document = Document.from_raw_text("")
                elif self._input_format == "jumanpp":
                    empty_document = Document.from_jumanpp("EOS\n")
                else:
                    assert self._input_format == "knp"
                    empty_document = Document.from_knp("EOS\n")
                _ = self.apply(empty_document)
        except Exception as e:
            logger.warning(f"failed to start KWJA: {e}")

    def is_available(self) -> bool:
        """KWJA が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    @override
    def apply_to_document(self, document: Union[Document, str], timeout: int = 30) -> Document:
        """文書に KWJA を適用する．

        Args:
            document: 文書．
            timeout: 最大処理時間．
        """
        if not self.is_available():
            raise RuntimeError("KWJA is not available.")

        if isinstance(document, str):
            document = Document(document)

        stdout_text: str = ""
        done_event: threading.Event = threading.Event()

        def worker() -> None:
            nonlocal stdout_text
            assert self._proc is not None
            assert self._proc.stdin is not None
            assert self._proc.stdout is not None
            assert self._proc.stderr is not None

            self._proc.stdin.write(self._gen_input_text(document))
            self._proc.stdin.flush()

            stdout_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                if line.strip() == Document.EOD:
                    break
                stdout_text += line

                # Non-blocking read from stderr
                stderr_text = ""
                while self._proc.stderr in select.select([self._proc.stderr], [], [], 0)[0]:
                    line = self._proc.stderr.readline()
                    if line.strip() == "":
                        break
                    stderr_text += line
                if stderr_text.strip() != "":
                    logger.warning(stderr_text.strip())
            done_event.set()

        with self._lock:
            thread = threading.Thread(target=worker)
            thread.start()
            done_event.wait(timeout)

            if thread.is_alive():
                thread.join()
                self.start_process(skip_sanity_check=True)
                raise TimeoutError(f"Operation timed out after {timeout} seconds.")

            if not self.is_available():
                self.start_process(skip_sanity_check=True)
                raise RuntimeError("KWJA exited unexpectedly.")

        return self._create_document(stdout_text)

    @override
    def apply_to_sentence(self, sentence: Union[Sentence, str], timeout: int = 10) -> Sentence:
        """文に KWJA を適用する．

        Args:
            sentence: 文．
            timeout: 最大処理時間．
        """
        raise NotImplementedError("KWJA does not support apply_to_sentence() currently.")

    def _gen_input_text(self, document: Document) -> str:
        if self._input_format == "raw":
            input_text = document.text.rstrip("\n") + "\n"
        elif self._input_format == "jumanpp":
            input_text = document.to_jumanpp()
        elif self._input_format == "knp":
            input_text = document.to_knp()
        else:
            raise AssertionError(f"invalid input format: {self._input_format}")
        return input_text + Document.EOD + "\n"

    def _create_document(self, text: str) -> Document:
        if self._output_format == "raw":
            return Document.from_raw_text(text)
        elif self._output_format == "jumanpp":
            return Document.from_jumanpp(text)
        elif self._output_format == "words":
            document = Document()
            sentences = []
            sentence_lines: List[str] = []
            for line in text.split("\n"):
                if line.strip() == "":
                    continue
                if is_comment_line(line) and sentence_lines:
                    sentences.append(self._create_sentence_from_words_format("\n".join(sentence_lines) + "\n"))
                    sentence_lines = []
                sentence_lines.append(line)
            sentences.append(self._create_sentence_from_words_format("\n".join(sentence_lines) + "\n"))
            document.sentences = sentences
            document.__post_init__()
            return document
        else:
            assert self._output_format == "knp"
            return Document.from_knp(text)

    @staticmethod
    def _create_sentence_from_words_format(text: str) -> Sentence:
        sentence = Sentence()
        morphemes: List[Morpheme] = []
        for line in text.split("\n"):
            if line.strip() == "":
                continue
            if is_comment_line(line):
                sentence.comment = line
                continue
            words: List[str] = line.split(" ")
            morphemes += [
                Morpheme(
                    text=word,
                    reading="*",
                    lemma="*",
                    pos="未定義語",
                    pos_id=15,
                    subpos="その他",
                    subpos_id=1,
                    conjtype="*",
                    conjtype_id=0,
                    conjform="*",
                    conjform_id=0,
                )
                for word in words
            ]
        sentence.morphemes = morphemes
        return sentence

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("KWJA is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8", check=True)
        return p.stdout.strip()

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        return [self.executable, *self.options]

    @property
    def version_command(self) -> List[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "--version"]
