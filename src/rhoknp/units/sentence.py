import re
from typing import TYPE_CHECKING, List, Optional, Union

from .chunk import Chunk
from .clause import Clause
from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit

if TYPE_CHECKING:
    from .document import Document


class Sentence(Unit):
    EOS = "EOS"
    count = 0

    def __init__(self):
        super().__init__()

        # parent unit
        self._document: Optional["Document"] = None

        # child units
        self._clauses: Optional[list[Clause]] = None
        self._morphemes: Optional[list[Morpheme]] = None

        self.sid: Optional[str] = None
        self.comment: Optional[str] = None

        self.index = self.count
        Sentence.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional["Document"]:
        return self._document

    @property
    def child_units(self) -> Optional[Union[list[Clause], list[Morpheme]]]:
        if self._clauses is not None:
            return self._clauses
        elif self._morphemes is not None:
            return self._morphemes
        return None

    @property
    def document(self) -> "Document":
        if self.parent_unit is None:
            raise AttributeError("document has not been set")
        return self.parent_unit

    @document.setter
    def document(self, document: "Document") -> None:
        self._document = document

    @property
    def clauses(self) -> list[Clause]:
        if self._clauses is None:
            raise AttributeError("not available before applying KNP")
        return self._clauses

    @clauses.setter
    def clauses(self, clauses: list[Clause]) -> None:
        for clause in clauses:
            clause.sentence = self
        self._clauses = clauses

    @property
    def chunks(self) -> list[Chunk]:
        return [chunk for clause in self.clauses for chunk in clause.chunks]

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        if self._morphemes is not None:
            return self._morphemes
        elif self._clauses is not None:
            return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]
        raise AttributeError("not available before applying Jumanpp")

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]) -> None:
        for morpheme in morphemes:
            morpheme.sentence = self
        self._morphemes = morphemes

    @property
    def need_jumanpp(self) -> bool:
        return self._morphemes is None

    @property
    def need_knp(self) -> bool:
        if self.need_jumanpp:
            return True
        return self._clauses is None

    @classmethod
    def from_string(cls, text: str) -> "Sentence":
        sentence = cls()
        sentence.text = text
        return sentence

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Sentence":
        sentence = cls()
        morphemes: List[Morpheme] = []
        jumanpp_lines: List[str] = []
        for line in jumanpp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("#"):
                if sentence.comment:
                    sentence.comment += "\n" + line
                else:
                    sentence.comment = line
                match = re.match(r"# S-ID: ?(\S*)( .+)?$", sentence.comment)
                if match:
                    sentence.sid = match.group(1)
                continue
            if line.startswith("@") and not line.startswith("@ @"):
                # homograph
                pass
            elif jumanpp_lines:
                morpheme = Morpheme.from_jumanpp("\n".join(jumanpp_lines))
                morphemes.append(morpheme)
                jumanpp_lines = []
            jumanpp_lines.append(line)
            if line.strip() == cls.EOS:
                break
        sentence.morphemes = morphemes
        return sentence

    @classmethod
    def from_knp(cls, knp_text: str) -> "Sentence":
        sentence = cls()
        clauses: list[Clause] = []
        clause_lines: list[str] = []
        is_clause_end = False
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("#"):
                if sentence.comment:
                    sentence.comment += "\n" + line
                else:
                    sentence.comment = line
                match = re.match(r"# S-ID: ?(\S*)( .+)?$", sentence.comment)
                if match:
                    sentence.sid = match.group(1)
                continue
            if line.startswith(";;"):
                raise Exception(f"Error: {line}")
            if line.startswith("+") and "節-区切" in line:
                is_clause_end = True
            if line.strip() == cls.EOS:
                clause = Clause.from_knp("\n".join(clause_lines))
                clauses.append(clause)
                break
            if line.startswith("*") and is_clause_end is True:
                clause = Clause.from_knp("\n".join(clause_lines))
                clauses.append(clause)
                clause_lines = []
                is_clause_end = False
            clause_lines.append(line)
        sentence.clauses = clauses
        return sentence

    def to_jumanpp(self) -> str:
        ret = ""
        if self.comment is not None:
            ret += self.comment + "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + self.EOS + "\n"
        return ret

    def to_knp(self) -> str:
        ret = ""
        if self.comment is not None:
            ret += self.comment + "\n"
        ret += "".join(clause.to_knp() for clause in self.clauses)
        ret += self.EOS + "\n"
        return ret
