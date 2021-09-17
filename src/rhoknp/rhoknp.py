from rhoknp.units import Document, Morpheme, Sentence


class Parser:
    def parse(self, text: str) -> Document:
        document = Document()
        document.parser = self
        document.text = text
        return document

    def load_jumanpp(self, analysis: str) -> Document:
        document = Document()
        document.parser = self
        sentences = []
        for analysis_for_sentence in analysis.split("EOS\n"):
            sentence = Sentence(document)
            self.assign_morphemes_to_sentence(sentence, analysis_for_sentence)
            sentences.append(sentence)
        document.sentences = sentences
        return document

    @staticmethod
    def assign_morphemes_to_sentence(sentence: Sentence, analysis: str):
        morphemes = []
        for line in analysis.split("\n"):
            if line.strip() != "EOS":
                morphemes.append(Morpheme(sentence, line))
        sentence.morphemes = morphemes


def parse(text: str) -> Document:
    parser = Parser()
    return parser.parse(text)


def load_jumanpp(analysis: str) -> Document:
    parser = Parser()
    return parser.load_jumanpp(analysis)


def load_knp(analysis: str) -> Document:
    return Document()
