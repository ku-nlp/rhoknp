from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp.units.document import Document


class Unit:
    def __init__(self, document: "Document"):
        self.document = document
