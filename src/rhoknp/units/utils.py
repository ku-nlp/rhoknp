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
    """コメント行なら True を返す．"""
    return line.startswith("# ") and not line.startswith("# # # 未定義語 15 その他 1 * 0 * 0")


class DepType(Enum):
    """文節，基本句の係り受けタイプを表す列挙体．"""

    DEPENDENCY = "D"
    PARALLEL = "P"
    APPOSITION = "A"
    IMPERFECT_PARALLEL = "I"


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


class Features(dict[str, Union[str, bool]]):
    """文節，基本句，形態素の素性情報を表すクラス．"""

    PAT = re.compile(r"(?P<feats>(<[^>]+>)*)")
    IGNORE_TAG_PREFIXES = {"rel "}
    FEATURE_PAT = re.compile(rf"<(?!({'|'.join(IGNORE_TAG_PREFIXES)}))(?P<key>[^:]+?)(:(?P<value>.+?))?>")

    @classmethod
    def from_fstring(cls, fstring: str) -> "Features":
        """素性文字列をパースして辞書型に変換する．
        e.g., "<正規化代表表記:遅れる/おくれる>" -> {"正規化代表表記": "遅れる/おくれる"}

        Args:
            fstring: KNP 形式における素性文字列．

        Returns: Features オブジェクト．

        """
        features = {}
        for match in cls.FEATURE_PAT.finditer(fstring):
            features[match.group("key")] = match.group("value") or True
        return cls(features)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
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
class Rel:
    """関係タグ付きコーパスにおける <rel> タグを表すクラス．"""

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


class Rels(list[Rel]):
    """関係タグ付きコーパスにおける <rel> タグの列を表すクラス．"""

    @classmethod
    def from_fstring(cls, fstring: str) -> "Rels":
        """KNP における素性文字列からオブジェクトを作成．"""
        rels = []
        for match in Rel.PAT.finditer(fstring):
            rels.append(
                Rel(
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


@dataclass
class DiscourseRelation:
    PAT: ClassVar[re.Pattern[str]] = re.compile(r"(?P<sid>.+?)/(?P<base_phrase_index>\d+?)/(?P<label>[^;]+);?")
    sid: str
    base_phrase_index: int
    label: str
    modifier: Optional["Clause"] = None
    head: Optional["Clause"] = None

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
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
        """素性文字列から初期化．

        Args:
            fstring: KNP 形式における素性文字列．

        Returns: DiscourseRelationList オブジェクト．

        """
        return cls(fstring)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return ";".join(map(str, self))

    def __str__(self) -> str:
        return self.to_fstring()
