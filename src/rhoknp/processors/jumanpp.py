from logging import Logger, getLogger
from subprocess import PIPE, Popen
from typing import Optional, Sequence, Union

from rhoknp.units import Document

from .processor import Processor
from .senter import RegexSenter

logger: Logger = getLogger(__file__)


class Jumanpp(Processor):
    def __init__(
        self,
        executor: Union[str, Sequence[str]] = "jumanpp",
        senter: Optional[Processor] = None,
    ):
        self.executor = executor
        self.senter = senter

    def apply(self, document: Union[Document, str]) -> Document:
        if isinstance(document, str):
            document = Document.from_string(document)

        if document.need_senter:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified when initializing KNP: use RegexSenter with no option")
                self.senter = RegexSenter()
            document = self.senter.apply(document)

        jumanpp_text = ""
        with Popen(self.executor, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.text)
                jumanpp_text += out
        return Document.from_jumanpp(jumanpp_text)
