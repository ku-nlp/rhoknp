from abc import ABC, abstractmethod
from typing import Callable, Union

from rhoknp.units.document import Document


class Processor(ABC):
    def __init__(self, executor: Union[Callable, str, list[str]]):
        self.executor = executor

    @abstractmethod
    def apply(self, document: Document) -> Document:
        """Apply document processing

        Args:
            document: Document

        Returns: Document

        """
        raise NotImplementedError
