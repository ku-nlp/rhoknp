import re

from .processor import Processor
from rhoknp.units.document import Document


class RegexSenter(Processor):
    """A sentence splitter. The code is mainly derived from python-textformatting:
    https://github.com/ku-nlp/python-textformatting
    """

    PERIODS = "。．？！♪☆★…?!"

    def __init__(self):
        super().__init__(None)

    def apply(self, document: Document) -> Document:
        """Apply document processing

        Args:
            document: Document

        Returns: Document

        """
        sentence_texts = self.split_document(document.text)
        ret_document = Document.from_sentences(sentence_texts)
        return ret_document

    def split_document(self, text: str) -> list[str]:
        """Split text into sentences by regular expressions."""
        base = f"[^{self.PERIODS}]*[f{self.PERIODS}]"
        eol = f"[^{self.PERIODS}]*$"
        regex = re.compile(f"{base}|{eol}$")
        candidates = []
        for line in text.split("\n"):
            candidates += re.findall(regex, line + "\n")
        candidates = self._merge_candidates(candidates)
        return self._clean_up_candidates(candidates)

    def _merge_candidates(self, candidates: list[str]) -> list[str]:
        """Merge sentence candidates."""
        candidates = self._merge_single_periods(candidates)
        candidates = self._merge_parenthesis(candidates)
        return candidates

    def _merge_single_periods(self, candidates: list[str]) -> list[str]:
        """Merge sentence candidates that consist of just a single period."""
        regex = re.compile(f"^[{self.PERIODS}]$")
        merged_candidates = [""]
        for candidate in candidates:
            if re.match(regex, candidate):
                merged_candidates[-1] += candidate
            else:
                merged_candidates.append(candidate)
        if merged_candidates[0] == "":
            merged_candidates.pop(0)  # remove the dummy sentence
        return merged_candidates

    @staticmethod
    def _merge_parenthesis(sentence_candidates: list[str]) -> list[str]:
        """Merge sentence candidates so that strings in parentheses or
        brackets are not split.
        """
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

        if prefix:
            merged_candidates.append(prefix)
        return merged_candidates

    @staticmethod
    def _clean_up_candidates(sentence_candidates: list[str]) -> list[str]:
        """Remove empty sentence candidates."""
        return [
            sentence_candidate.strip()
            for sentence_candidate in sentence_candidates
            if sentence_candidate.strip()
        ]
