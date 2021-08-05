from typing import TYPE_CHECKING, Union

from rhoknp.units.phrase import Phrase
from rhoknp.units.sentence import Sentence
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.clause import Clause


class Morpheme(Unit):
    def __init__(self, parent: Union[Sentence, Phrase], analysis: str):
        super().__init__(parent.document)
        if isinstance(parent, Sentence):
            self.sentence = parent
            self.__clause = None
            self.__chunk = None
            self.__phrase = None
        elif isinstance(parent, Phrase):
            self.sentence = parent.sentence
            self.__clause = parent.clause
            self.__chunk = parent.chunk
            self.__phrase = parent

        self.__analysis = analysis

        self.__index: int = None
        self.__text: str = None
        self.__reading: str = None
        self.__lemma: str = None
        self.__canon: str = None
        self.__pos: str = None
        self.__pos_: int = None
        self.__subpos: str = None
        self.__subpos_: int = None
        self.__conjtype: str = None
        self.__conjtype_: int = None
        self.__conjform: str = None
        self.__conjform_: int = None
        self.__features: dict[str, str] = None
        self.___features: dict[str, str] = None

    @property
    def clause(self):
        return self.__clause

    @clause.setter
    def clause(self, clause: "Clause"):
        self.__clause = clause

    @property
    def chunk(self):
        return self.__chunk

    @chunk.setter
    def chunk(self, chunk: "Chunk"):
        self.__chunk = chunk

    @property
    def phrase(self):
        return self.__clause

    @phrase.setter
    def phrase(self, phrase: Phrase):
        self.__phrase = phrase

    @property
    def index(self):
        self.set_attributes()
        return self.__index

    @property
    def text(self):
        self.set_attributes()
        return self.__text

    @property
    def reading(self):
        self.set_attributes()
        return self.__reading

    @property
    def lemma(self):
        self.set_attributes()
        return self.__lemma

    @property
    def canon(self):
        self.set_attributes()
        return self.__canon

    @property
    def pos(self):
        self.set_attributes()
        return self.__pos

    @property
    def pos_(self):
        self.set_attributes()
        return self.__pos_

    @property
    def subpos(self):
        self.set_attributes()
        return self.__subpos

    @property
    def subpos_(self):
        self.set_attributes()
        return self.__subpos_

    @property
    def conjtype(self):
        self.set_attributes()
        return self.__conjtype

    @property
    def conjtype_(self):
        self.set_attributes()
        return self.__conjtype_

    @property
    def conjform(self):
        self.set_attributes()
        return self.__conjform

    @property
    def conjform_(self):
        self.set_attributes()
        return self.__conjform_

    @property
    def features(self):
        self.set_attributes()
        return self.__features | self.___features

    @property
    def _features(self):
        self.set_attributes()
        return self.___features

    def set_attributes(self):
        if self.__index is not None:
            return
        parts = self.__analysis.split(" ", maxsplit=11)
        self.__index = 0  # TODO
        self.__text = parts[0]
        self.__reading = parts[1]
        self.__lemma = parts[2]
        self.__pos = parts[3]
        self.__pos_ = int(parts[4])
        self.__subpos = parts[5]
        self.__subpos_ = int(parts[6])
        self.__conjtype = parts[7]
        self.__conjtype_ = int(parts[8])
        self.__conjform = parts[9]
        self.__conjform_ = int(parts[10])
        self.__features = {}
        features = {}
        for feat in parts[11].strip('"').split(" "):
            key, value = feat.split(":")
            features[key] = value
        self.___features = features

    def to_jumanpp(self) -> str:
        features = [f"{key}:{value}" for key, value in self._features.items()]
        if len(features) > 0:
            features = '"' + " ".join(features) + '"'
        else:
            features = "NIL"
        return " ".join(
            [
                self.text,
                self.reading,
                self.lemma,
                self.pos,
                str(self.pos_),
                self.subpos,
                str(self.subpos_),
                self.conjtype,
                str(self.conjtype_),
                self.conjform,
                str(self.conjform_),
                features,
            ]
        )
