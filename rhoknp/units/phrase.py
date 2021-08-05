from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.morpheme import Morpheme


class Phrase:
    def __init__(self, chunk: Chunk, analysis: str):
        self.document = chunk.document
        self.sentence = chunk.sentence
        self.clause = chunk.clause
        self.chunk = chunk

        self.__analysis = analysis

        self.__morphemes: list[Morpheme] = None

    @property
    def morphemes(self):
        return self.__morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]):
        self.__morphemes = morphemes
