from logging import getLogger
from subprocess import PIPE, Popen
from typing import Optional, Sequence, Union

from rhoknp.units import Document, Sentence

from .jumanpp import Jumanpp
from .processor import Processor
from .senter import RegexSenter

logger = getLogger(__file__)


class KNP(Processor):
    def __init__(
        self,
        executor: Union[str, Sequence[str]] = ["knp", "-tab"],
        senter: Optional[Processor] = None,
        jumanpp: Optional[Processor] = None,
    ):
        self.executor = executor
        self.senter = senter
        self.jumanpp = jumanpp

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        if isinstance(document, str):
            document = Document(document)

        if document.need_senter:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug(
                    "senter is not specified when initializing KNP: use RegexSenter with no option"
                )
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        if document.need_jumanpp:
            logger.debug("document needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info(
                    "jumanpp is not specified when initializing KNP: use Jumanpp with no option"
                )
                self.jumanpp = Jumanpp()
            document = self.jumanpp.apply_to_document(document)

        knp_text = ""
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.to_jumanpp())
                knp_text += out
        return Document.from_knp(knp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.need_jumanpp:
            logger.debug("sentence needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info(
                    "jumanpp is not specified when initializing KNP: use Jumanpp with no option"
                )
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence)

        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            knp_text, _ = p.communicate(input=sentence.to_jumanpp())
        return Sentence.from_knp(knp_text)
