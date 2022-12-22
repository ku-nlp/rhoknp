import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, List, Optional

CASE_TYPES = [
    "ガ",
    "デ",
    "ト",
    "ニ",
    "ノ",
    "ヘ",
    "ヲ",
    "カラ",
    "ガ２",
    "ノ？",
    "マデ",
    "ヨリ",
    "トイウ",
    "トシテ",
    "トスル",
    "ニオク",
    "ニシテ",
    "ニツク",
    "ニトル",
    "ニヨル",
    "マデニ",
    "ニオイテ",
    "ニカワル",
    "ニソッテ",
    "ニツイテ",
    "ニトッテ",
    "ニムケテ",
    "ニムケル",
    "ニヨッテ",
    "ニヨラズ",
    "ニアワセテ",
    "ニカギッテ",
    "ニカギラズ",
    "ニカランデ",
    "ニカワッテ",
    "ニカンシテ",
    "ニカンスル",
    "ニクラベテ",
    "ニクワエテ",
    "ニタイシテ",
    "ニタイスル",
    "ニツヅイテ",
    "ニナランデ",
    "ヲツウジテ",
    "ヲツウジル",
    "ヲノゾイテ",
    "ヲフクメテ",
    "ヲメグッテ",
    "ニトモナッテ",
    "ニモトヅイテ",
    "無",
    "修飾",
    "判ガ",
    "時間",
    "外の関係",
]
CASE_TYPES += [case + "≒" for case in CASE_TYPES]

COREF_TYPES = ["=", "=構", "=役"]
COREF_TYPES += [coref + "≒" for coref in COREF_TYPES]

logger = logging.getLogger(__name__)


class RelMode(Enum):
    """同一の基本句に同一タイプの関係タグが複数付いている場合にそれらの関係を表す列挙体．

    .. note::
        各関係タグの具体例は以下の通りである：

        * AND
            （例）太郎と花子が学校から<帰った>（ガ格:太郎, ガ格:花子 [and]）
        * OR
            （例）私は田園調布か国立に<住みたい>（ガ格:私, ニ格:田園調布, ニ格:国立 [or]）
        * AMBIGUOUS
            （例）高知県の橋本知事は…国籍条項を<撤廃する>方針を明らかにした（ガ格:高知県, ガ格:橋本知事 [？], ガ格:不特定:人 [？], ヲ格:条項, 外の関係:方針）

    .. note::
        target が「なし」の場合，同じタイプの関係タグが任意的要素であることを示す．
            （例）太郎は一人で<立っていた>（ガ格:太郎, デ格:一人, デ格:なし [？]）
    """

    AND = "AND"  #: 関係の対象が並列である．
    OR = "OR"  #: 「AかB」のように意味的に or である．
    AMBIGUOUS = "？"  #: いずれの解釈も妥当であり，文脈から判断ができない．


@dataclass(frozen=True)
class RelTag:
    """関係タグ付きコーパスにおける <rel> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern] = re.compile(
        r'<rel type="(?P<type>\S+?)"( mode="(?P<mode>\S+?)")? target="(?P<target>.+?)"( sid="(?P<sid>.*?)" '
        r'id="(?P<id>\d+?)")?/>'
    )
    type: str
    target: str
    sid: Optional[str]
    base_phrase_index: Optional[int]
    mode: Optional[RelMode]

    def __post_init__(self):
        if self.type.startswith("="):
            if self.type not in COREF_TYPES:
                logger.warning(f"Unknown coreference type: {self.type} ({self})")
        else:
            if self.type not in CASE_TYPES:
                logger.warning(f"Unknown case type: {self.type} ({self})")

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        ret = f'<rel type="{self.type}"'
        if self.mode is not None:
            ret += f' mode="{self.mode.value}"'
        ret += f' target="{self.target}"'
        if self.sid is not None:
            assert self.base_phrase_index is not None
            ret += f' sid="{self.sid}" id="{self.base_phrase_index}"'
        ret += "/>"
        return ret


class RelTagList(List[RelTag]):
    """関係タグ付きコーパスにおける <rel> タグの列を表すクラス．"""

    @classmethod
    def from_fstring(cls, fstring: str) -> "RelTagList":
        """KNP における素性文字列からオブジェクトを作成．"""
        rel_tags = []
        for match in RelTag.PAT.finditer(fstring):
            rel_tags.append(
                RelTag(
                    type=match["type"],
                    target=match["target"],
                    sid=match["sid"],
                    base_phrase_index=int(match["id"]) if match["id"] else None,
                    mode=RelMode(match["mode"]) if match["mode"] else None,
                )
            )
        return cls(rel_tags)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return "".join(rel_tag.to_fstring() for rel_tag in self)

    def __str__(self) -> str:
        return self.to_fstring()
