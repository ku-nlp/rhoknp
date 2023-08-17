import logging
import select
import subprocess
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

from rhoknp.processors.jumanpp import Jumanpp
from rhoknp.processors.processor import Processor
from rhoknp.processors.senter import RegexSenter
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class KNP(Processor):
    """KNP クラス．

    Args:
        executable: KNP のパス．
        options: KNP のオプション．
        senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割する．
            未設定なら RegexSenter を使って文分割する．
        jumanpp: Jumanpp のインスタンス．形態素解析がまだなら，先にこのインスタンスを用いて形態素解析する．
            未設定なら Jumanpp （オプションなし）を使って形態素解析する．

    Example:
        >>> from rhoknp import KNP
        >>> knp = KNP()
        >>> document = knp.apply("電気抵抗率は電気の通しにくさを表す物性値である。")

    .. note::
        使用するには `KNP <https://github.com/ku-nlp/knp>`_ がインストールされている必要がある．
    """

    def __init__(
        self,
        executable: str = "knp",
        options: Optional[List[str]] = None,
        senter: Optional[Processor] = None,
        jumanpp: Optional[Processor] = None,
        skip_sanity_check: bool = False,
    ) -> None:
        self.executable = executable  #: KNP のパス．
        self.options = options or ["-tab"]  #: KNP のオプション．
        if "-tab" not in self.options:
            raise ValueError("`-tab` option is required when you use KNP. ")
        self.senter = senter
        self.jumanpp = jumanpp
        self._proc: Optional[Popen] = None
        self._lock = Lock()
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
            if skip_sanity_check is False:
                _ = self.apply(Sentence.from_jumanpp(""))
        except Exception as e:
            logger.warning(f"failed to start KNP: {e}")

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        if self.jumanpp is not None:
            arg_string += f", jumanpp={repr(self.jumanpp)}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        if self._proc is not None:
            self._proc.kill()

    def is_available(self) -> bool:
        """KNP が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に KNP を適用する．

        Args:
            document: 文書．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None

        if isinstance(document, str):
            document = Document(document)

        if document.is_senter_required() is True:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
                logger.debug(self.senter)
            document = self.senter.apply_to_document(document)

        sentences: List[Sentence] = []
        for sentence in document.sentences:
            sentences.append(self.apply_to_sentence(sentence))
        return Document.from_sentences(sentences)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に KNP を適用する．

        Args:
            sentence: 文．

        .. note::
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None
        assert self._proc.stderr is not None

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.is_jumanpp_required() is True:
            logger.debug("sentence needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info("jumanpp is not specified when initializing KNP: use Jumanpp with no option")
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence)

        with self._lock:
            self._proc.stdin.write(sentence.to_jumanpp() if sentence.is_knp_required() is True else sentence.to_knp())
            self._proc.stdin.flush()
            stdout_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                stdout_text += line
                if line.strip() == Sentence.EOS:
                    break

                # Non-blocking read from stderr
                stderr_text = ""
                while self._proc.stderr in select.select([self._proc.stderr], [], [], 0)[0]:
                    stderr_text += self._proc.stderr.readline()
                if stderr_text.strip() != "":
                    raise ValueError(line.strip())
            return Sentence.from_knp(stdout_text)

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8")
        return p.stderr.strip()

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        return [self.executable] + self.options

    @property
    def version_command(self) -> List[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "-v"]
