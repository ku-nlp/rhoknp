from abc import ABC, abstractmethod

from rhoknp.units.document import Document


class Processor(ABC):
    @abstractmethod
    def apply(self, document: Document) -> Document:
        """Apply document processing

        Args:
            document: Document

        Returns: Document

        """
        raise NotImplementedError
