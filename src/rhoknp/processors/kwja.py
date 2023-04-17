import logging
import subprocess
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

from rhoknp.processors.processor import Processor
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class KWJA(Processor):
    """KWJA クラス．

    Args:
        executable: KWJA のパス．
        options: KWJA のオプション．

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
    ) -> None:
        self.executable = executable  #: KWJA のパス．
        self.options: List[str] = options or []  #: KWJA のオプション．
        self._proc: Optional[Popen] = None
        self._output_format = "knp"
        if "--tasks" in self.options:
            tasks: List[str] = self.options[self.options.index("--tasks") + 1].split(",")
            if "word" in tasks:
                self._output_format = "knp"
            elif "char" in tasks:
                self._output_format = "words"
                raise ValueError(f"`--tasks {','.join(tasks)}` option is not supported yet in rhoknp.")
            elif "seq2seq" in tasks:
                self._output_format = "seq2seq"
            elif "typo" in tasks:
                self._output_format = "raw"
            else:
                raise ValueError(f"invalid task: {tasks}")
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        except Exception as e:
            logger.warning(f"failed to start KWJA: {e}")
        self._lock = Lock()

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options:
            arg_string += f", options={repr(self.options)}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        if self._proc is not None:
            self._proc.kill()

    def is_available(self) -> bool:
        """KWJA が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に KWJA を適用する．

        Args:
            document: 文書．
        """
        if not self.is_available():
            raise RuntimeError("KWJA is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None

        if isinstance(document, str):
            document = Document(document)

        with self._lock:
            self._proc.stdin.write(document.text.rstrip("\n") + "\n")  # TODO: Keep the sentence IDs
            self._proc.stdin.write(Document.EOD + "\n")
            self._proc.stdin.flush()
            out_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                if line.strip() == Document.EOD:
                    break
                out_text += line
            if self._output_format == "raw":
                return Document.from_raw_text(out_text)
            elif self._output_format == "seq2seq":
                return Document.from_jumanpp(out_text)
            else:
                assert self._output_format == "knp"
                return Document.from_knp(out_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に KWJA を適用する．

        Args:
            sentence: 文．
        """
        if not self.is_available():
            raise RuntimeError("KWJA is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with self._lock:
            self._proc.stdout.flush()
            self._proc.stdin.write(sentence.text.rstrip("\n") + "\n")  # TODO: Keep the sentence ID
            self._proc.stdin.write(Document.EOD + "\n")
            self._proc.stdin.flush()
            out_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                if line.strip() == Document.EOD:
                    break
                out_text += line
            if self._output_format == "raw":
                return Sentence.from_raw_text(out_text)
            elif self._output_format == "seq2seq":
                return Sentence.from_jumanpp(out_text)
            else:
                assert self._output_format == "knp"
                return Sentence.from_knp(out_text)

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("KWJA is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8")
        return p.stdout.strip()

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        return [self.executable] + self.options

    @property
    def version_command(self) -> List[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "--version"]
