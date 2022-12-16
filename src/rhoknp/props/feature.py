import logging
import re
from typing import Dict, Union

logger = logging.getLogger(__name__)


class FeatureDict(Dict[str, Union[str, bool]]):
    """文節，基本句，形態素の素性情報を表すクラス．"""

    IGNORE_TAG_PREFIXES = {"rel ", "memo "}
    PAT = re.compile(r'(?P<feats>(<([^>"]|"[^"]*?")+>)*)')
    FEATURE_PAT = re.compile(rf"<(?!({'|'.join(IGNORE_TAG_PREFIXES)}))(?P<key>([^:\"]|\".*?\")+?)(:(?P<value>.+?))?>")

    def __setitem__(self, key: str, value: Union[str, bool]) -> None:
        if key == "rel":
            logger.warning(
                f"Adding 'rel' to {self.__class__.__name__} is not supported and was ignored. Instead, add a RelTag "
                f"object to BasePhrase.rel_tags and call Document.reparse()."
            )
            return
        if key == "memo":
            logger.warning(
                f"Adding 'memo' to {self.__class__.__name__} is not supported and was ignored. Instead, set a MemoTag "
                f"object to BasePhrase.memo_tag."
            )
            return
        super().__setitem__(key, value)

    @classmethod
    def from_fstring(cls, fstring: str) -> "FeatureDict":
        """素性文字列をパースして辞書型に変換する．

        例："<正規化代表表記:遅れる/おくれる>" -> {"正規化代表表記": "遅れる/おくれる"}

        Args:
            fstring: KNP 形式における素性文字列．
        """
        features = {}
        for match in cls.FEATURE_PAT.finditer(fstring):
            features[match["key"]] = match["value"] or True
        return cls(features)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return "".join(self._item_to_fstring(k, v) for k, v in self.items())

    @staticmethod
    def _item_to_fstring(key: str, value: Union[str, bool]) -> str:
        if value is False:
            return ""
        if value is True:
            return f"<{key}>"
        return f"<{key}:{value}>"
