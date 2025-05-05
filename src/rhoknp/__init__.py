from importlib.metadata import version

from rhoknp.processors import KNP, KWJA, Jumanpp, RegexSenter
from rhoknp.units import BasePhrase, Clause, Document, Morpheme, Phrase, Sentence

__version__ = version("rhoknp")

__all__ = [
    "KNP",
    "KWJA",
    "BasePhrase",
    "Clause",
    "Document",
    "Jumanpp",
    "Morpheme",
    "Phrase",
    "RegexSenter",
    "Sentence",
    "__version__",
]
