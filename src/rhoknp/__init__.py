from importlib.metadata import version

from rhoknp.processors import KNP, KWJA, Jumanpp, RegexSenter
from rhoknp.units import BasePhrase, Clause, Document, Morpheme, Phrase, Sentence

__version__ = version("rhoknp")

__all__ = [
    "__version__",
    "RegexSenter",
    "Jumanpp",
    "KNP",
    "KWJA",
    "Document",
    "Sentence",
    "Clause",
    "Phrase",
    "BasePhrase",
    "Morpheme",
]
