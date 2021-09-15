import copy
from subprocess import Popen, PIPE
from typing import Union, Callable

from rhoknp.units import Document, Sentence
from .processor import Processor


class Jumanpp(Processor):
    def __init__(self, executor: Union[Callable, str] = "jumanpp"):
        super().__init__(executor)

    def apply(self, document: Document):
        ret_document = copy.deepcopy(document)
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            sentences = []
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.text)
                sentences.append(Sentence.from_jumanpp(out))
            document.sentences = sentences
            document.text = ''.join(str(s) for s in sentences)
        return ret_document
