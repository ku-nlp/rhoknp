from typing import TYPE_CHECKING, Optional

from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.sentence import Sentence


class Morpheme(Unit):

    count = 0

    def __init__(self, analysis: str, sentence: Optional["Sentence"] = None):
        super().__init__(sentence)
        self.analysis = analysis

        self.sentence = self.parent_unit
        self.clause = None
        self.chunk = None
        self.phrase = None

        parts = self.analysis.split(" ", maxsplit=11)

        self.index = self.count

        self.text = parts[0]
        self.reading = parts[1]
        self.lemma = parts[2]
        self.pos = parts[3]
        self.pos_ = int(parts[4])
        self.subpos = parts[5]
        self.subpos_ = int(parts[6])
        self.conjtype = parts[7]
        self.conjtype_ = int(parts[8])
        self.conjform = parts[9]
        self.conjform_ = int(parts[10])
        self.features = {}
        for feature in parts[11].strip('"').split(" "):
            if feature == "NIL":
                break
            if ":" in feature:
                key, value = feature.split(":", maxsplit=1)
            else:
                key, value = feature, True
            self.features[key] = value

        Morpheme.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        return None

    def to_jumanpp(self) -> str:
        features = [
            key if isinstance(value, bool) else f"{key}:{value}"
            for key, value in self.features.items()
        ]
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
