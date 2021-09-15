from typing import List, Union

from rhoknp.units.sentence import Sentence
from rhoknp.units.unit import Unit


class Document(Unit):
    def __init__(self):
        super().__init__(self)
        self.__text: str = None

        self.__sentences: list["Sentence"] = None

    @property
    def text(self):
        if self.__text is not None:
            return self.__text
        else:
            return "".join(str(m) for m in self.morphemes)

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def sentences(self):
        return self.__sentences

    @sentences.setter
    def sentences(self, sentences: list["Sentence"]):
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
        doc = cls()
        doc.text = text
        return doc

    @classmethod
    def from_sentence(cls, sentence: Union[Sentence, str]) -> "Document":
        doc = cls()
        if isinstance(sentence, str):
            sentence = Sentence.from_string(sentence)
        sentence.document = doc
        doc.sentences = [sentence]
        doc.text = str(sentence)
        return doc

    @classmethod
    def from_sentences(cls, sentences: List[Union[Sentence, str]]) -> "Document":
        doc = cls()
        sents = []
        for sentence in sentences:
            if isinstance(sentence, str):
                sentence = Sentence.from_string(sentence)
            sentence.document = doc
            sents.append(sentence)
        doc.sentences = sentences
        doc.text = "".join(str(s) for s in sentences)
        return doc
