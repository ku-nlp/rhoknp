from abc import ABC, abstractmethod
from multiprocessing import Pool

from rhoknp.units.document import Document


class Processor(ABC):
    @abstractmethod
    def apply(self, document: Document) -> Document:
        raise NotImplementedError

    def batch_apply(self, documents: list[Document], processes: int = 0) -> list[Document]:
        if processes < 1:
            return list(map(self.apply, documents))

        with Pool(processes=processes) as pool:
            return pool.map(self.apply, documents)
