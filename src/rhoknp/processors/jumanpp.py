from logging import getLogger
from subprocess import PIPE, Popen, run
from typing import Optional, Union

from rhoknp.units import Document, Sentence

from .processor import Processor
from .senter import RegexSenter

logger = getLogger(__file__)


class Jumanpp(Processor):
    def __init__(
        self,
        executable: str = "jumanpp",
        senter: Optional[Processor] = None,
    ):
        self.executable = executable
        self.senter = senter

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        if isinstance(document, str):
            document = Document.from_string(document)

        if document.need_senter:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified when initializing KNP: use RegexSenter with no option")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        jumanpp_text = ""
        with Popen(self.executable, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            for sentence in document.sentences:
                out, _ = p.communicate(input=sentence.text)
                jumanpp_text += out
        return Document.from_jumanpp(jumanpp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        if isinstance(sentence, str):
            sentence = Sentence.from_string(sentence)

        with Popen(self.executable, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=sentence.text)
        return Sentence.from_jumanpp(jumanpp_text)

    def is_available(self):
        try:
            p = run([self.executable, "-v"], stdout=PIPE, stdin=PIPE, encoding="utf-8")
            logger.info(p.stdout.strip())
            return True
        except Exception as e:
            logger.warning(e)
            return False
