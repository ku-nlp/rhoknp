import re
from typing import TYPE_CHECKING, Optional, Union

from .clause import Clause
from .morpheme import Morpheme

from .unit import Unit

if TYPE_CHECKING:
    from .document import Document


class Sentence(Unit):
    EOS = "EOS"
    count = 0

    def __init__(self, document: Optional["Document"] = None):
        super().__init__(document)

        self.index = self.count

        self.comment: str = None
        self.clauses: list["Clause"] = None
        self.morphemes: list["Morpheme"] = None

        Sentence.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Union[list[Clause], list[Morpheme]]:
        if self.clauses is not None:
            return self.clauses
        else:
            return self.morphemes

    def to_jumanpp(self):
        jumanpp_text = ""
        if self.comment is not None:
            jumanpp_text += self.comment + "\n"
        jumanpp_text += (
            "\n".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
            + "\n"
            + self.EOS
        )
        return jumanpp_text

    @classmethod
    def from_string(
        cls, text: str, document: Optional["Document"] = None
    ) -> "Sentence":
        sentence = cls(document)
        sentence.text = text
        return sentence

    @classmethod
    def from_jumanpp(
        cls, jumanpp_text: str, document: Optional["Document"] = None
    ) -> "Sentence":
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
    def from_knp(cls, knp_text: str, parent: Optional["Document"] = None) -> "Sentence":
        sentence = cls(parent)
        clauses: list[Clause] = []
        clause_lines: list[str] = []
        for line in knp_text.split("\n"):
            if line.strip() == "":
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
            if line.strip() == cls.EOS:
                clause = Clause.from_knp("\n".join(clause_lines), parent=sentence)
                clauses.append(clause)
                break
            # TODO: find clause boundary
            if line.startswith("*"):
                if clause_lines:
                    clause = Clause.from_knp("\n".join(clause_lines), parent=sentence)
                    clauses.append(clause)
                    clause_lines = []
            clause_lines.append(line)

        sentence.clauses = clauses
        return sentence
