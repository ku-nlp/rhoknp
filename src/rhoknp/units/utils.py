import re
from typing import Union


class Semantics(dict):
    NIL = "NIL"
    PATTERN: re.Pattern = re.compile(r'(?P<sems>("([^"]|\\")+?")|NIL)')
    SEM_PATTERN: re.Pattern = re.compile(r"(?P<key>[^:]+)(:(?P<value>\S+))?\s?")

    def __init__(self, sstring: str):
        super().__init__()
        self.is_nil = sstring == self.NIL
        if not self.is_nil:
            for match in self.SEM_PATTERN.finditer(sstring.strip('"')):
                self[match.group("key")] = match.group("value") or True

    @classmethod
    def from_sstring(cls, sstring) -> "Semantics":
        return cls(sstring)

    def to_sstring(self) -> str:
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


class Features(dict):
    """A class to represent a feature information for a chunk or a phrase

    This class parses tags in features string and converts to a dictionary.
    ex. "<正規化代表表記:遅れる/おくれる>" --> {"正規化代表表記": "遅れる/おくれる"}
    """

    PATTERN: re.Pattern = re.compile(r"(?P<feats>(<.+>)*)")
    TAG_PATTERN: re.Pattern = re.compile(r"<(?P<key>[^:]+?)(:(?P<value>.+?))?>")

    def __init__(self, fstring: str):
        super().__init__()
        for match in self.TAG_PATTERN.finditer(fstring):
            self[match.group("key")] = match.group("value") or True

    @classmethod
    def from_fstring(cls, fstring) -> "Features":
        return cls(fstring)

    def to_fstring(self) -> str:
        return "".join(self._item2tag_string(k, v) for k, v in self.items())

    @staticmethod
    def _item2tag_string(key: str, value: Union[str, bool]) -> str:
        if value is False:
            return ""
        if value is True:
            return f"<{key}>"
        return f"<{key}:{value}>"

    def __str__(self) -> str:
        return self.to_fstring()
