import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Optional, Union

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.sentence import Sentence

logger = logging.getLogger(__name__)


def is_comment_line(line: str) -> bool:
    return line.startswith("# ") and not line.startswith("# # # 未定義語 15 その他 1 * 0 * 0")


class DepType(Enum):
    DEPENDENCY = "D"
    PARALLEL = "P"
    APPOSITION = "A"
    IMPERFECT_PARALLEL = "I"


class Semantics(dict[str, Union[str, bool]]):
    NIL = "NIL"
    PAT = re.compile(r'(?P<sems>("([^"]|\\")+?")|NIL)')
    SEM_PAT = re.compile(r"(?P<key>[^:]+)(:(?P<value>\S+))?\s?")

    def __init__(self, sstring: str):
        super().__init__()
        self.is_nil = sstring == self.NIL
        if not self.is_nil:
            for match in self.SEM_PAT.finditer(sstring.strip('"')):
                self[match.group("key")] = match.group("value") or True

    @classmethod
    def from_sstring(cls, sstring: str) -> "Semantics":
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


class Features(dict[str, Union[str, bool]]):
    """A class to represent a feature information for a phrase or a base phrase

    This class parses tags in features string and converts to a dictionary.
    ex. "<正規化代表表記:遅れる/おくれる>" --> {"正規化代表表記": "遅れる/おくれる"}
    """

    PAT = re.compile(r"(?P<feats>(<[^>]+>)*)")
    IGNORE_TAG_PREFIXES = {"rel "}
    FEATURE_PAT = re.compile(rf"<(?!({'|'.join(IGNORE_TAG_PREFIXES)}))(?P<key>[^:]+?)(:(?P<value>.+?))?>")

    def __init__(self, fstring: str):
        super().__init__()
        for match in self.FEATURE_PAT.finditer(fstring):
            self[match.group("key")] = match.group("value") or True

    @classmethod
    def from_fstring(cls, fstring: str) -> "Features":
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
    PAT: ClassVar[re.Pattern[str]] = re.compile(
        r'<rel type="(?P<type>\S+?)"( mode="(?P<mode>[^>]+?)")? target="(?P<target>.+?)"( sid="(?P<sid>.*?)" '
        r'id="(?P<id>\d+?)")?/>'
    )
    type: str
    target: str
    sid: Optional[str]
    base_phrase_index: Optional[int]
    mode: Optional[RelMode]

    def to_fstring(self) -> str:
        ret = f'<rel type="{self.type}"'
        if self.mode is not None:
            ret += f' mode="{self.mode.value}"'
        ret += f' target="{self.target}"'
        if self.sid is not None:
            assert self.base_phrase_index is not None
            ret += f' sid="{self.sid}" id="{self.base_phrase_index}"'
        ret += "/>"
        return ret


class Rels(list[Rel]):
    def __init__(self, fstring: str):
        super().__init__()
        for match in Rel.PAT.finditer(fstring):
            self.append(
                Rel(
                    type=match["type"],
                    target=match["target"],
                    sid=match["sid"],
                    base_phrase_index=int(match["id"]) if match["id"] else None,
                    mode=RelMode(match["mode"]) if match["mode"] else None,
                )
            )

    @classmethod
    def from_fstring(cls, fstring: str) -> "Rels":
        return cls(fstring)

    def to_fstring(self) -> str:
        return "".join(rel.to_fstring() for rel in self)

    def __str__(self) -> str:
        return self.to_fstring()


@dataclass
class DiscourseRelation:
    PAT: ClassVar[re.Pattern[str]] = re.compile(r"(?P<sid>.+?)/(?P<base_phrase_index>\d+?)/(?P<label>[^;]+);?")
    sid: str
    base_phrase_index: int
    label: str
    modifier: Optional["Clause"] = None
    head: Optional["Clause"] = None

    def to_fstring(self) -> str:
        return f"{self.sid}/{self.base_phrase_index}/{self.label}"

    def __str__(self) -> str:
        return self.to_fstring()


class DiscourseRelationList(list[DiscourseRelation]):
    def __init__(self, fstring: str, clause: Optional["Clause"] = None):
        super().__init__()
        for match in DiscourseRelation.PAT.finditer(fstring):
            sid = match["sid"]
            base_phrase_index = int(match["base_phrase_index"])
            label = match["label"]
            modifier: Optional["Clause"] = None
            head: Optional["Clause"] = None
            if clause:
                modifier = clause
                head_sentence: Optional["Sentence"] = None
                for sentence in clause.document.sentences:
                    if sentence.sid == sid:
                        head_sentence = sentence
                        break
                if head_sentence is None:
                    logger.warning(f"{sid} not found")
                    continue
                if base_phrase_index >= len(head_sentence.base_phrases):
                    logger.warning(f"index out of range in {sid}")
                    continue
                head_base_phrase = head_sentence.base_phrases[base_phrase_index]
                head = head_base_phrase.clause
                if head.end != head_base_phrase:
                    logger.warning(f"invalid clause tag in {sid}")
                    continue
            self.append(
                DiscourseRelation(
                    sid=sid,
                    base_phrase_index=base_phrase_index,
                    label=label,
                    modifier=modifier,
                    head=head,
                )
            )

    @classmethod
    def from_fstring(cls, fstring: str) -> "DiscourseRelationList":
        return cls(fstring)

    def to_fstring(self) -> str:
        return ";".join(map(str, self))

    def __str__(self) -> str:
        return self.to_fstring()
