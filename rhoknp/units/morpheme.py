from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.phrase import Phrase


class Morpheme:
    def __init__(self, phrase: Phrase, analysis: str):
        self.document = phrase.document
        self.sentence = phrase.sentence
        self.clause = phrase.clause
        self.chunk = phrase.chunk
        self.phrase = phrase

        self.__analysis = analysis
