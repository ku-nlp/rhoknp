import logging
import re
import threading
from typing import ClassVar, List, Union

try:
    from typing import override  # type: ignore
except ImportError:
    from typing_extensions import override

from rhoknp.processors.processor import Processor
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class RegexSenter(Processor):
    """正規表現にもとづく文分割クラス．

    Example:
        >>> from rhoknp import RegexSenter
        >>> senter = RegexSenter()
        >>> document = senter.apply("天気が良かったので散歩した。途中で先生に会った。")
    """

    _PERIOD_PAT: ClassVar[re.Pattern] = re.compile(r"[。．？！♪☆★…?!]+")  #: ピリオドとみなすパターン．

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @override
    def apply_to_document(self, document: Union[Document, str], timeout: int = 10) -> Document:
        """文書に RegexSenter を適用する．

        Args:
            document: 文書．
            timeout: 最大処理時間．．
        """
        if isinstance(document, str):
            document = Document(document)
        doc_id = document.doc_id

        sentences: List[str] = []
        done_event: threading.Event = threading.Event()

        def worker() -> None:
            nonlocal sentences
            sentences = self._split_document(document.text)
            done_event.set()

        thread = threading.Thread(target=worker)
        thread.start()
        done_event.wait(timeout)

        if thread.is_alive():
            raise TimeoutError("Operation timed out.")

        ret = Document.from_sentences(sentences)
        if doc_id != "":
            ret.doc_id = doc_id
            for sentence in ret.sentences:
                sentence.doc_id = doc_id
        return ret

    @override
    def apply_to_sentence(self, sentence: Union[Sentence, str], timeout: int = 10) -> Sentence:
        """文に RegexSenter を適用する．

        Args:
            sentence: 文．
            timeout: 最大処理時間．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)
        return sentence

    def _split_document(self, text: str) -> List[str]:
        if text == "":
            return []

        def split_text_by_period(text: str) -> List[str]:
            segments: List[str] = []
            start: int = 0
            for match in self._PERIOD_PAT.finditer(text):
                end: int = match.end()
                segments.append(text[start:end])
                start = end
            if start < len(text):
                segments.append(text[start:])
            return [segment.strip() for segment in segments]

        sentences: List[str] = []
        for line in text.split("\n"):
            # Split by periods
            sentence_candidates: List[str] = split_text_by_period(line)

            # Merge sentence candidates so that strings in parentheses or brackets are not split
            parenthesis_level: int = 0
            hook_bracket_level: int = 0
            double_hook_bracket_level: int = 0
            sentence: str = ""
            while sentence_candidates:
                sentence_candidate: str = sentence_candidates.pop(0)

                sentence += sentence_candidate

                parenthesis_level += sentence_candidate.count("（") - sentence_candidate.count("）")
                parenthesis_level += sentence_candidate.count("(") - sentence_candidate.count(")")
                hook_bracket_level += sentence_candidate.count("「") - sentence_candidate.count("」")
                double_hook_bracket_level += sentence_candidate.count("『") - sentence_candidate.count("』")
                if parenthesis_level == hook_bracket_level == double_hook_bracket_level == 0:
                    if sentence.strip():
                        sentences.append(sentence.strip())
                    sentence = ""
            if sentence.strip():
                sentences.extend(split_text_by_period(sentence.strip()))

        return sentences
