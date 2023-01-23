import re
from typing import Dict, Optional, Union


class SemanticsDict(Dict[str, Union[str, bool]]):
    """形態素の意味情報を表すクラス．"""

    NIL = "NIL"
    PAT = re.compile(rf'(?P<sems>("[^"]+?")|{NIL})')
    SEM_PAT = re.compile(r"(?P<key>[^:\s]+)(:(?P<value>\S+))?(\s|$)")

    def __init__(self, semantics: Optional[Dict[str, Union[str, bool]]] = None, is_nil: bool = False) -> None:
        if semantics is None:
            semantics = {}
        super().__init__(semantics)
        self.is_nil: bool = is_nil

    @classmethod
    def from_sstring(cls, sstring: str) -> "SemanticsDict":
        """意味情報文字列をパースして辞書型に変換する．

        例："代表表記:日本/にほん 地名:国" -> {"代表表記": "日本/にほん", "地名": "国"}

        Args:
            sstring: KNP 形式における意味情報文字列．
        """
        is_nil = sstring == cls.NIL
        semantics = {}
        if not is_nil:
            for match in cls.SEM_PAT.finditer(sstring.strip('"')):
                semantics[match["key"]] = match["value"] or True
        return cls(semantics, is_nil)

    def to_sstring(self) -> str:
        """意味情報文字列に変換．"""
        if len(self) == 0:
            return "" if self.is_nil is False else self.NIL
        return f'"{" ".join(self._item_to_sstring(k, v) for k, v in self.items())}"'

    @staticmethod
    def _item_to_sstring(key: str, value: Union[str, bool]) -> str:
        if value is False:
            return ""
        if value is True:
            return f"{key}"
        return f"{key}:{value}"
