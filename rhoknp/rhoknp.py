from rhoknp.units import Document, Morpheme, Sentence


def parse(text: str) -> Document:
    doc = Document()
    doc.text = text
    return doc


def load_jumanpp(analysis: str) -> Document:
    document = Document()
    sentences = []
    sentence = Sentence(document)
    morphemes = []
    for line in analysis.split("\n"):
        if line.strip() == "EOS":
            sentence.morphemes = morphemes
            sentences.append(sentence)
            sentence = Sentence(document)
            morphemes = []
        morphemes.append(Morpheme(sentence, line))
    document.sentences = sentences
    return document


def load_knp(analysis: str) -> Document:
    return Document()
