from subprocess import PIPE, Popen
from typing import Callable, Union

from rhoknp.processors.processor import Processor
from rhoknp.units import Document, Sentence


class Jumanpp(Processor):
    def __init__(self, executor: Union[Callable, str] = "jumanpp"):
        super().__init__(executor)

    def apply(self, document: Document):
        ret_document = Document()
        ret_document.text = document.text
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            sentences = []
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.text)
                sentences.append(Sentence.from_jumanpp(out))
            document.sentences = sentences
        return ret_document
