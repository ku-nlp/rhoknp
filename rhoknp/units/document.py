from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.sentence import Sentence


class Document:
    def __init__(self):
        self.__text: str = None
        self.__sentences: list[Sentence] = None

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
    def sentences(self, sentences: str):
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
