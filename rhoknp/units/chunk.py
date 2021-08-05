from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.phrase import Phrase


class Chunk:
    def __init__(self, parent: "Clause", analysis: str):
        self.document = parent.document
        self.sentence = parent.sentence
        self.clause = parent

        self.__analysis = analysis

        self.__phrases: list["Phrase"] = None

    @property
    def phrases(self):
        return self.__phrases

    @phrases.setter
    def phrases(self, phrases: list["Phrase"]):
        self.__phrases = phrases

    @property
    def morphemes(self):
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]
