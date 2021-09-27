from subprocess import PIPE, Popen
from typing import Callable, Union

from rhoknp.units import Document

from .processor import Processor


class KNP(Processor):
    def __init__(self, executor: Union[Callable, str, list[str]] = ["knp", "-tab"]):
        super().__init__(executor)

    def apply(self, document: Document) -> Document:
        knp_text = ""
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.to_jumanpp())
                knp_text += out
        ret_document = Document.from_knp(knp_text)
        return ret_document
