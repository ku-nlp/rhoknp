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

    PERIODS = "。．？！♪☆★…?!"  #: ピリオドとみなす文字．

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
        """Split text into sentences by regular expressions."""
        base = f"[^{self.PERIODS}]*[f{self.PERIODS}]"
        eol = f"[^{self.PERIODS}]*$"
        regex = re.compile(f"{base}|{eol}$")
        candidates = []
        for line in text.split("\n"):
            candidates += re.findall(regex, line + "\n")
        candidates = self._merge_candidates(candidates)
        return self._clean_up_candidates(candidates)

    def _merge_candidates(self, candidates: List[str]) -> List[str]:
        """Merge sentence candidates."""
        candidates = self._merge_single_periods(candidates)
        candidates = self._merge_parenthesis(candidates)
        return candidates

    def _merge_single_periods(self, candidates: List[str]) -> List[str]:
        """Merge sentence candidates that consist of just a single period."""
        regex = re.compile(f"^[{self.PERIODS}]$")
        merged_candidates = [""]
        for candidate in candidates:
            if re.match(regex, candidate) is not None:
                merged_candidates[-1] += candidate
            else:
                merged_candidates.append(candidate)
        if merged_candidates[0] == "":
            merged_candidates.pop(0)  # remove the dummy sentence
        return merged_candidates

    @staticmethod
    def _merge_parenthesis(sentence_candidates: List[str]) -> List[str]:
        """Merge sentence candidates so that strings in parentheses or brackets are not split."""
        parenthesis_level = 0
        quotation_level = 0

        merged_candidates = []
        prefix = ""
        while sentence_candidates:
            candidate = sentence_candidates.pop(0)

            parenthesis_level += candidate.count("（") + candidate.count("(")
            parenthesis_level -= candidate.count("）") + candidate.count(")")

            quotation_level += candidate.count("「") + candidate.count("“")
            quotation_level -= candidate.count("」") + candidate.count("”")

            if parenthesis_level == 0 and quotation_level == 0:
                candidate = prefix + candidate
                merged_candidates.append(candidate)
                prefix = ""
            else:
                if "\n" in candidate:
                    candidate, rest = candidate.split("\n", maxsplit=1)
                    candidate = prefix + candidate
                    merged_candidates.append(candidate)
                    prefix = ""
                    sentence_candidates.insert(0, rest)
                    parenthesis_level = 0
                    quotation_level = 0
                else:
                    prefix += candidate

        if prefix != "":
            merged_candidates.append(prefix)
        return merged_candidates

    @staticmethod
    def _clean_up_candidates(sentence_candidates: List[str]) -> List[str]:
        """Remove empty sentence candidates."""
        return [sentence_candidate.strip() for sentence_candidate in sentence_candidates if sentence_candidate.strip()]
