from typing import Optional

from rhoknp.units import Phrase


class Predicate:
    def __init__(self, unit: Phrase, cfid: Optional[str] = None):
        self.unit: Phrase = unit
        self.cfid = cfid
