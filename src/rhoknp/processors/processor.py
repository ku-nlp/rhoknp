from abc import ABC
from typing import Callable, Union

from rhoknp.units.document import Document


class Processor(ABC):
    def __init__(self, executor: Union[Callable, str]):
        self.executor = executor

    def apply(self, document: Document) -> Document:
        """Apply document processing

        Args:
            document: Document

        Returns: Document

        """
        raise NotImplementedError
