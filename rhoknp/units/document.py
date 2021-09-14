from typing import TYPE_CHECKING

from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.rhoknp import Parser
    from rhoknp.units.sentence import Sentence


class Document(Unit):
    def __init__(self):
        super().__init__(self)
        self.__text: str = None

        self.__sentences: list["Sentence"] = None

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def sentences(self):
        return self.__sentences

    @sentences.setter
    def sentences(self, sentences: list["Sentence"]):
        self.__sentences = sentences

    @property
    def clauses(self):
        return [clause for sentence in self.sentences for clause in sentence.clauses]

    @property
    def chunks(self):
        return [chunk for sentence in self.sentences for chunk in sentence.chunks]

    @property
    def phrases(self):
        return [phrase for sentence in self.sentences for phrase in sentence.phrases]

    @property
    def morphemes(self):
        return [
            morpheme for sentence in self.sentences for morpheme in sentence.morphemes
        ]

    def to_jumanpp(self) -> str:
        return "\n".join(sentence.to_jumanpp() for sentence in self.sentences)

    @classmethod
    def from_string(cls, text: str) -> "Document":
        doc = cls()
        doc.text = text
        return doc
