from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.sentence import Sentence


class Clause:
    def __init__(self, sentence: Sentence):
        self.document = sentence.document
        self.sentence = sentence

        self.__chunks: list[Chunk] = None

    @property
    def chunks(self):
        return self.__chunks

    @chunks.setter
    def chunks(self, chunks: list[Chunk]):
        self.__chunks = chunks

    @property
    def phrases(self):
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self):
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]
