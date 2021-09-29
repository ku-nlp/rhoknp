from typing import List, Union

from .chunk import Chunk
from .clause import Clause
from .morpheme import Morpheme
from .phrase import Phrase
from .sentence import Sentence
from .unit import Unit


class Document(Unit):
    count = 0

    def __init__(self):
        super().__init__(None)

        Sentence.count = 0
        Clause.count = 0
        Chunk.count = 0
        Phrase.count = 0
        Morpheme.count = 0

        self.__sentences: list[Sentence] = None

        self.index = self.count
        Document.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> list[Sentence]:
        return self.sentences

    @property
    def sentences(self) -> list[Sentence]:
        return self.__sentences

    @sentences.setter
    def sentences(self, sentences: list[Sentence]) -> None:
        self.__sentences = sentences

    @property
    def clauses(self) -> list[Clause]:
        return [clause for sentence in self.sentences for clause in sentence.clauses]

    @property
    def chunks(self) -> list[Chunk]:
        return [chunk for clause in self.clauses for chunk in clause.chunks]

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for sentence in self.sentences for morpheme in sentence.morphemes]

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
        sentence_lines: list[str] = []
        for line in jumanpp_text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if line.strip() == Sentence.EOS:
                sentences.append(Sentence.from_jumanpp("\n".join(sentence_lines) + "\n", document))
                sentence_lines = []
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
                sentences.append(Sentence.from_knp("\n".join(sentence_lines) + "\n", document))
                sentence_lines = []
        document.sentences = sentences
        return document

    def to_jumanpp(self) -> str:
        return "\n".join(sentence.to_jumanpp() for sentence in self.sentences)

    def to_knp(self) -> str:
        ret = ""
        for sentence in self.sentences:
            ret += sentence.to_knp()
        return ret
