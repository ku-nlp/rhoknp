import re
from typing import TYPE_CHECKING, Optional, Union

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

    def __init__(self, document: Optional["Document"] = None):
        super().__init__(document)

        self.comment: str = None
        self.__clauses: list[Clause] = None
        self.__morphemes: list[Morpheme] = None

        self.index = self.count
        Sentence.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Union[list[Clause], list[Morpheme], None]:
        if self.__clauses is not None:
            return self.clauses
        elif self.__morphemes is not None:
            return self.morphemes
        return None

    @property
    def document(self) -> "Document":
        if self.parent_unit is None:
            raise AttributeError("This attribute has not been set")
        return self.parent_unit

    @property
    def clauses(self) -> list[Clause]:
        if self.__clauses is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self.__clauses

    @clauses.setter
    def clauses(self, clauses: list[Clause]) -> None:
        self.__clauses = clauses

    @property
    def chunks(self) -> list[Chunk]:
        return [chunk for clause in self.clauses for chunk in clause.chunks]

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        if self.__morphemes is not None:
            return self.__morphemes
        elif self.__clauses is not None:
            return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]
        else:
            raise AttributeError("This attribute is not available before applying Jumanpp")

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]) -> None:
        self.__morphemes = morphemes

    def to_jumanpp(self) -> str:
        jumanpp_text = ""
        if self.comment is not None:
            jumanpp_text += self.comment + "\n"
        jumanpp_text += "\n".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + "\n" + self.EOS + "\n"
        return jumanpp_text

    @classmethod
    def from_string(cls, text: str, document: Optional["Document"] = None) -> "Sentence":
        sentence = cls(document)
        sentence.text = text
        return sentence

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str, document: Optional["Document"] = None) -> "Sentence":
        sentence = cls(document)
        morphemes = []
        for line in jumanpp_text.split("\n"):
            if line.startswith("#"):
                if sentence.comment:
                    sentence.comment += "\n" + line
                else:
                    sentence.comment = line
            if line.strip() == cls.EOS:
                break
            morphemes.append(Morpheme.from_jumanpp(line, sentence))
        sentence.morphemes = morphemes
        return sentence

    @classmethod
    def from_knp(cls, knp_text: str, document: Optional["Document"] = None) -> "Sentence":
        sentence = cls(document)
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
                clause = Clause.from_knp("\n".join(clause_lines), sentence)
                clauses.append(clause)
                break
            if line.startswith("*") and is_clause_end is True:
                clause = Clause.from_knp("\n".join(clause_lines), sentence)
                clauses.append(clause)
                clause_lines = []
                is_clause_end = False
            clause_lines.append(line)
        sentence.clauses = clauses
        return sentence

    def to_knp(self) -> str:
        ret = self.comment + "\n"
        for clause in self.clauses:
            ret += clause.to_knp()
        ret += self.EOS + "\n"
        return ret
