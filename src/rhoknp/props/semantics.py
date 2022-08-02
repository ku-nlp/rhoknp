import re
from typing import Union


class Semantics(dict[str, Union[str, bool]]):
    """形態素の意味情報を表すクラス．"""

    NIL = "NIL"
    PAT = re.compile(rf'(?P<sems>("([^"]|\\")+?")|{NIL})')
    SEM_PAT = re.compile(r"(?P<key>[^:]+)(:(?P<value>\S+))?\s?")

    def __init__(self, semantics: dict[str, Union[str, bool]] = None, is_nil: bool = False):
        if semantics is None:
            semantics = {}
        super().__init__(semantics)
        self.is_nil: bool = is_nil

    @classmethod
    def from_sstring(cls, sstring: str) -> "Semantics":
        """意味情報文字列をパースして辞書型に変換する．
        e.g., "\"代表表記:日本/にほん 地名:国\"" -> {"代表表記": "日本/にほん", "地名": "国"}

        Args:
            sstring: KNP 形式における意味情報文字列．

        Returns: Features オブジェクト．

        """
        is_nil = sstring == cls.NIL
        semantics = {}
        if not is_nil:
            for match in cls.SEM_PAT.finditer(sstring.strip('"')):
                semantics[match.group("key")] = match.group("value") or True
        return cls(semantics, is_nil)

    def to_sstring(self) -> str:
        """意味情報文字列に変換．"""
        if self.is_nil:
            return self.NIL
        if len(self) == 0:
            return ""
        return f'"{" ".join(self._item2sem_string(k, v) for k, v in self.items())}"'

    @staticmethod
    def _item2sem_string(key: str, value: Union[str, bool]) -> str:
        if value is False:
            return ""
        if value is True:
            return f"{key}"
        return f"{key}:{value}"

    def __str__(self) -> str:
        return self.to_sstring()

    def __bool__(self) -> bool:
        return bool(dict(self)) or self.is_nil
