from importlib.metadata import version

from rhoknp.processors import KNP, Jumanpp, RegexSenter
from rhoknp.units import BasePhrase, Clause, Document, Morpheme, Phrase, Sentence

__version__ = version("rhoknp")

__all__ = [
    "__version__",
    # processors
    "RegexSenter",
    "Jumanpp",
    "KNP",
    # units
    "Document",
    "Sentence",
    "Clause",
    "Phrase",
    "BasePhrase",
    "Morpheme",
]
