import logging
import re
from typing import Union

logger = logging.getLogger(__name__)


class FeatureDict(dict[str, Union[str, bool]]):
    """文節，基本句，形態素の素性情報を表すクラス．"""

    PAT = re.compile(r"(?P<feats>(<[^>]+>)*)")
    IGNORE_TAG_PREFIXES = {"rel ", "NE:", "談話関係:"}
    FEATURE_PAT = re.compile(rf"<(?!({'|'.join(IGNORE_TAG_PREFIXES)}))(?P<key>[^:]+?)(:(?P<value>.+?))?>")

    @classmethod
    def from_fstring(cls, fstring: str) -> "FeatureDict":
        """素性文字列をパースして辞書型に変換する．
        e.g., "<正規化代表表記:遅れる/おくれる>" -> {"正規化代表表記": "遅れる/おくれる"}

        Args:
            fstring: KNP 形式における素性文字列．
        """
        features = {}
        for match in cls.FEATURE_PAT.finditer(fstring):
            features[match.group("key")] = match.group("value") or True
        return cls(features)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return "".join(self._item_to_fstring(k, v) for k, v in self.items())

    def __setitem__(self, key, value) -> None:
        if key == "rel":
            logger.warning(
                f"Adding 'rel' to {self.__class__.__name__} is not supported and was ignored. Instead, add a Rel "
                f"object to BasePhrase.rels and call Document.reparse()."
            )
            return
        if key == "NE":
            logger.warning(
                f"Adding 'NE' to {self.__class__.__name__} is not supported and was ignored. Instead, append a "
                f"NamedEntity object to Sentence.named_entities."
            )
            return
        if key == "談話関係":
            logger.warning(
                f"Adding '談話関係' to {self.__class__.__name__} is not supported and was ignored. Instead, append a "
                f"DiscourseRelation object to the Clause object."
            )
        super().__setitem__(key, value)

    @staticmethod
    def _item_to_fstring(key: str, value: Union[str, bool]) -> str:
        if value is False:
            return ""
        if value is True:
            return f"<{key}>"
        return f"<{key}:{value}>"

    def __str__(self) -> str:
        return self.to_fstring()
