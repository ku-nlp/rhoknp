import logging
import re
from typing import List, Union

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

    _PERIOD_PAT = re.compile(r"[。．？！♪☆★…?!]+")  #: ピリオドとみなすパターン．

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に RegexSenter を適用する．

        Args:
            document: 文書．
        """
        if isinstance(document, str):
            document = Document(document)
        sentence_texts = self._split_document(document.text)
        return Document.from_sentences(sentence_texts)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に RegexSenter を適用する．

        Args:
            sentence: 文．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)
        return sentence

    def _split_document(self, text: str) -> List[str]:
        if text == "":
            return []

        sentences: List[str] = []
        for line in text.split("\n"):
            # Split by periods
            sentence_candidates: List[str] = []
            start: int = 0
            for match in self._PERIOD_PAT.finditer(line):
                end: int = match.end()
                sentence_candidates.append(line[start:end])
                start = end
            if start < len(line):
                sentence_candidates.append(line[start:])

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
                sentences.append(sentence.strip())

        return sentences
