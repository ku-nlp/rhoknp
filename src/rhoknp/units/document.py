from typing import List, Union

from .unit import Unit
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.sentence import Sentence


class Document(Unit):
    def __init__(self):
        super().__init__(self)

        Sentence.count = 0
        Morpheme.count = 0

        self.__text: str = None
        self.__sentences: list[Sentence] = None

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> list[Sentence]:
        return self.sentences

    @property
    def text(self):
        if self.__text is not None:
            return self.__text
        else:
            return "".join(str(child_unit) for child_unit in self.child_units)

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def sentences(self):
        return self.__sentences

    @sentences.setter
    def sentences(self, sentences: list[Sentence]):
        self.__sentences = sentences

    @property
    def clauses(self):
        return [clause for sentence in self.sentences for clause in sentence.clauses]

    @property
    def chunks(self):
        return [chunk for sentence in self.sentences for chunk in sentence.chunks]

    @property
    def phrases(self):
        return [phrase for sentence in self.sentences for phrase in sentence.phrases]

    @property
    def morphemes(self):
        return [
            morpheme for sentence in self.sentences for morpheme in sentence.morphemes
        ]

    def to_jumanpp(self) -> str:
        return "\n".join(sentence.to_jumanpp() for sentence in self.sentences)

    @classmethod
    def from_string(cls, text: str) -> "Document":
        document = cls()
        document.text = text
        return document

    @classmethod
    def from_sentence(cls, sentence: Union[Sentence, str]) -> "Document":
        document = cls()
        if isinstance(sentence, str):
            sentence = Sentence.from_string(sentence, document)
        document.sentences = [sentence]
        return document

    @classmethod
    def from_sentences(cls, sentences: List[Union[Sentence, str]]) -> "Document":
        document = cls()
        sentences_ = []
        for sentence in sentences:
            if isinstance(sentence, str):
                sentence = Sentence.from_string(sentence, document)
            sentences_.append(sentence)
        document.sentences = sentences_
        return document

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Document":
        document = cls()
        sentences = []
        for jumanpp_text_sentence in jumanpp_text.split(Sentence.EOS):
            jumanpp_text_sentence = jumanpp_text_sentence.strip()
            if not jumanpp_text_sentence:
                continue
            sentences.append(Sentence.from_jumanpp(jumanpp_text_sentence, document))
        document.sentences = sentences
        return document

    @classmethod
    def from_knp(cls, knp_text: str) -> "Document":
        document = cls()
        sentences = []
        sentence_lines: list[str] = []
        for line in knp_text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if line.strip() == Sentence.EOS:
                sentences.append(Sentence.from_knp("\n".join(sentence_lines) + "\n", parent=document))
                sentence_lines = []
        document.sentences = sentences
        return document