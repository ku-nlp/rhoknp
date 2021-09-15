from subprocess import PIPE, Popen
from typing import Callable, Union

from rhoknp.processors.processor import Processor
from rhoknp.units import Document


class Jumanpp(Processor):
    def __init__(self, executor: Union[Callable, str] = "jumanpp"):
        super().__init__(executor)

    def apply(self, document: Document):
        jumanpp_text = ""
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.text)
                jumanpp_text += out
        ret_document = Document.from_jumanpp(jumanpp_text)
        return ret_document
