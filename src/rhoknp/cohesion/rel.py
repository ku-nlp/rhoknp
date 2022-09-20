import re
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, List, Optional


class RelMode(Enum):
    """同一の基本句に同一タイプの関係タグが複数付いている場合にそれらの関係を表す列挙体．

        * AND: 関係の対象が並列である．
            (例) 太郎と花子が学校から<帰った> (ガ格:太郎, ガ格:花子 [and])
        * OR: 「AかB」のように意味的に or である．
            (例) 私は田園調布か国立に<住みたい> (ガ格:私, ニ格:田園調布, ニ格:国立 [or])
        * AMBIGUOUS:いずれの解釈も妥当であり，文脈から判断ができない．
            (例) 高知県の橋本知事は…国籍条項を<撤廃する>方針を明らかにした (ガ格:高知県, ガ格:橋本知事 [？], ガ格:不特定:人 [？], ヲ格:条項, 外の関係:方針)

    Notes:
        target が「なし」の場合、同じタイプの関係タグが任意的要素であることを示す．
            (例) 太郎は一人で<立っていた> (ガ格:太郎, デ格:一人, デ格:なし [？])
    """

    AND = "AND"
    OR = "OR"
    AMBIGUOUS = "？"


@dataclass
class RelTag:
    """関係タグ付きコーパスにおける <rel> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern] = re.compile(
        r'<rel type="(?P<type>\S+?)"( mode="(?P<mode>[^>]+?)")? target="(?P<target>.+?)"( sid="(?P<sid>.*?)" '
        r'id="(?P<id>\d+?)")?/>'
    )
    type: str
    target: str
    sid: Optional[str]
    base_phrase_index: Optional[int]
    mode: Optional[RelMode]

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
        rels = []
        for match in RelTag.PAT.finditer(fstring):
            rels.append(
                RelTag(
                    type=match["type"],
                    target=match["target"],
                    sid=match["sid"],
                    base_phrase_index=int(match["id"]) if match["id"] else None,
                    mode=RelMode(match["mode"]) if match["mode"] else None,
                )
            )
        return cls(rels)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return "".join(rel.to_fstring() for rel in self)

    def __str__(self) -> str:
        return self.to_fstring()
