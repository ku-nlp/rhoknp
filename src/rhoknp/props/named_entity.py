import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp.units.morpheme import Morpheme

logger = logging.getLogger(__name__)


class NamedEntityCategory(Enum):
    """固有表現カテゴリを表す列挙体．"""

    ORGANIZATION = "ORGANIZATION"
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ARTIFACT = "ARTIFACT"
    DATE = "DATE"
    TIME = "TIME"
    MONEY = "MONEY"
    PERCENT = "PERCENT"
    OPTIONAL = "OPTIONAL"
    NONE = "NONE"  #: NE-OPTIONAL の候補カテゴリにのみ使用する．

    @classmethod
    def has_value(cls, value: str) -> bool:
        """有効な固有表現カテゴリであれば True．

        Args:
            value: 固有表現のカテゴリ．
        """
        return any(value == item.value for item in cls)


@dataclass
class NamedEntity:
    """固有表現を表すクラス．

    .. note::
        possible_categories は候補カテゴリを注釈順に格納する．
        NONE は固有表現として抽出しない解釈を表す．

        optional_type の 0 は他の理由に該当しない場合，1 は語源まで遡る必要がある場合，
        2 は空想上の表現で固有名としての扱いが曖昧な場合，3 は人を表す役職名，
        4 は肩書を含む慣用的な人名表現を表す．
    """

    PAT: ClassVar[re.Pattern] = re.compile(r"<NE:(?P<cat>\w+):(?P<name>([^>\\]|\\>?)+)>")
    OPTIONAL_PAT: ClassVar[re.Pattern] = re.compile(r"<NE-OPTIONAL:(?P<cats>\w+(?:,\w+)*):(?P<type>[0-4])>")

    category: NamedEntityCategory  #: 固有表現カテゴリ．
    morphemes: list["Morpheme"]  #: 固有表現を構成する形態素のリスト．
    possible_categories: list[NamedEntityCategory] = field(
        default_factory=list
    )  #: OPTIONAL の候補カテゴリ．NE-OPTIONAL がなければ空リスト．
    optional_type: int | None = None  #: OPTIONAL になった理由を表すコード．NE-OPTIONAL がなければ None．

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        """固有表現の表層文字列．"""
        return "".join(m.text for m in self.morphemes)

    @classmethod
    def from_fstring(cls, fstring: str, candidate_morphemes: list["Morpheme"]) -> Optional["NamedEntity"]:
        """NE と任意の NE-OPTIONAL を含む素性文字列からオブジェクトを作成．

        NE の直後にある NE-OPTIONAL を読み取る．
        読み取った注釈に不整合がある場合は警告を出力し，None を返す．
        """
        match = cls.PAT.match(fstring)
        if match is None:
            logger.warning(f"{fstring} is not a valid NE fstring")
            return None
        category: str = match["cat"]
        if not NamedEntityCategory.has_value(category) or category == "NONE":
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: invalid NE category: {category}")
            return None
        name: str = match["name"].replace(r"\>", ">")
        span = cls._find_morpheme_span(name, candidate_morphemes)
        if span is None:
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: morpheme span of '{name}' not found")
            return None
        possible_categories: list[NamedEntityCategory] = []
        optional_type: int | None = None
        optional_match = cls.OPTIONAL_PAT.match(fstring, match.end())
        if optional_match is not None:
            if category != "OPTIONAL":
                logger.warning(f"{candidate_morphemes[0].sentence.sid}: NE-OPTIONAL requires the OPTIONAL category")
                return None
            for possible_category in optional_match["cats"].split(","):
                if not NamedEntityCategory.has_value(possible_category) or possible_category == "OPTIONAL":
                    logger.warning(
                        f"{candidate_morphemes[0].sentence.sid}: invalid NE-OPTIONAL category: {possible_category}"
                    )
                    return None
                possible_categories.append(NamedEntityCategory(possible_category))
            optional_type = int(optional_match["type"])
        return NamedEntity(
            NamedEntityCategory(category),
            candidate_morphemes[span.start : span.stop],
            possible_categories,
            optional_type,
        )

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        escaped_text = self.text.replace(">", r"\>")  # escape ">"
        fstring = f"<NE:{self.category.value}:{escaped_text}>"
        if self.optional_type is not None:
            categories = ",".join(category.value for category in self.possible_categories)
            fstring += f"<NE-OPTIONAL:{categories}:{self.optional_type}>"
        return fstring

    @staticmethod
    def _find_morpheme_span(name: str, candidates: list["Morpheme"]) -> range | None:
        """固有表現の文字列にマッチする形態素の範囲を返す．

        Args:
            name: 固有表現の文字列
            candidates: 固有表現を構成する候補形態素のリスト
        """
        stop = len(candidates)
        while stop > 0:
            for start in reversed(range(stop)):
                if "".join(m.text for m in candidates[start:stop]) == name:
                    return range(start, stop)
            stop -= 1
        return None
