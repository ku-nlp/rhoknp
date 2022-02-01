from importlib.metadata import version

from rhoknp.processors import KNP, Jumanpp, RegexSenter
from rhoknp.units import BasePhrase, Chunk, Clause, Document, Morpheme, Sentence

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
    "Chunk",
    "BasePhrase",
    "Morpheme",
]
