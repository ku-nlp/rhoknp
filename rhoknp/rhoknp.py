from rhoknp.units import Document
from rhoknp.utils import Format


def parse(text: str) -> Document:
    doc = Document()
    doc.text = text
    return doc


def load(analysis: str, fmt: Format) -> Document:
    return Document()


def load_jumanpp(analysis: str) -> Document:
    return load(analysis, Format.JUMANPP)


def load_knp(analysis: str) -> Document:
    return load(analysis, Format.KNP)
