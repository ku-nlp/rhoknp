import re
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional, Union


class DepType(Enum):
    DEPENDENCY = "D"
    PARALLEL = "P"
    APPOSITION = "A"
    IMPERFECT_PARALLEL = "I"


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

    def __bool__(self) -> bool:
        return bool(dict(self)) or self.is_nil


class Features(dict):
    """A class to represent a feature information for a chunk or a phrase

    This class parses tags in features string and converts to a dictionary.
    ex. "<正規化代表表記:遅れる/おくれる>" --> {"正規化代表表記": "遅れる/おくれる"}
    """

    PATTERN: re.Pattern = re.compile(r"(?P<feats>(<[^>]+>)*)")
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


class RelMode(Enum):
    """同一の基本句に同一タイプの関係タグが複数付いている場合にそれらの関係を表す

        * AND: 関係の対象が並列である
            (例) 太郎と花子が学校から<帰った> (ガ格:太郎, ガ格:花子 [and])
        * OR: 「AかB」のように意味的に or である
            (例) 私は田園調布か国立に<住みたい> (ガ格:私, ニ格:田園調布, ニ格:国立 [or])
        * AMBIGUOUS:いずれの解釈も妥当であり、文脈から判断ができない
            (例) 高知県の橋本知事は…国籍条項を<撤廃する>方針を明らかにした (ガ格:高知県, ガ格:橋本知事 [？], ガ格:不特定:人 [？], ヲ格:条項, 外の関係:方針)

    Notes:
        target が「なし」の場合、同じタイプの関係タグが任意的要素であることを示す
            (例) 太郎は一人で<立っていた> (ガ格:太郎, デ格:一人, デ格:なし [？])
    """

    AND = "AND"
    OR = "OR"
    AMBIGUOUS = "？"


@dataclass
class Rel:
    PATTERN: ClassVar[re.Pattern] = re.compile(
        r'<rel type="(?P<type>\S+?)"( mode="(?P<mode>[^>]+?)")? target="(?P<target>.+?)"( sid="(?P<sid>.+?)" '
        r'id="(?P<id>\d+?)")?/>'
    )
    type: str
    target: str
    sid: Optional[str]
    phrase_index: Optional[int]
    mode: Optional[RelMode]

    def to_fstring(self) -> str:
        ret = f'<rel type="{self.type}"'
        if self.mode is not None:
            ret += f' mode="{self.mode.value}"'
        ret += f' target="{self.target}"'
        if self.sid is not None:
            assert self.phrase_index is not None
            ret += f' sid="{self.sid}" id="{self.phrase_index}"'
        ret += "/>"
        return ret


class Rels(list):
    def __init__(self, fstring: str):
        super().__init__()
        for match in Rel.PATTERN.finditer(fstring):
            self.append(
                Rel(
                    type=match["type"],
                    target=match["target"],
                    sid=match["sid"],
                    phrase_index=match["id"] and int(match["id"]),
                    mode=match["mode"] and RelMode(match["mode"]),
                )
            )

    @classmethod
    def from_fstring(cls, fstring: str) -> "Rels":
        return cls(fstring)

    def to_fstring(self) -> str:
        return "".join(rel.to_fstring() for rel in self)

    def __str__(self) -> str:
        return self.to_fstring()
