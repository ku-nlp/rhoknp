import logging
import re
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union

from rhoknp.props.named_entity import NamedEntity
from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.clause import Clause
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.phrase import Phrase
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.document import Document

logger = logging.getLogger(__name__)


class Sentence(Unit):
    """文クラス．

    Args:
        text: 文の文字列．
    """

    EOS = "EOS"
    SID_PAT = re.compile(r"^(?P<sid>(?P<did>[a-zA-Z\d\-_]+?)(-(\d+))?)$")
    SID_PAT_KWDLC = re.compile(r"^(?P<sid>(?P<did>w\d{6}-\d{10})(-\d+){1,2})$")
    SID_PAT_WAC = re.compile(r"^(?P<sid>(?P<did>wiki\d{8})(-\d{2})(-\d{2})?)$")
    count = 0

    def __init__(self, text: Optional[str] = None):
        super().__init__()
        if text is not None:
            self.text = text.replace("\r", "").replace("\n", "")

        Clause.count = 0
        Phrase.count = 0
        BasePhrase.count = 0
        Morpheme.count = 0

        # parent unit
        self._document: Optional["Document"] = None

        # child units
        self._clauses: Optional[List[Clause]] = None
        self._phrases: Optional[List[Phrase]] = None
        self._morphemes: Optional[List[Morpheme]] = None

        self._sent_id: Optional[str] = None
        self._doc_id: Optional[str] = None
        self.misc_comment: str = ""

        self.named_entities: List[NamedEntity] = []

        self.index = self.count  #: 文書全体におけるインデックス．
        Sentence.count += 1

    def __post_init__(self) -> None:
        super().__post_init__()

        # Find named entities in the sentence.
        self.named_entities = []
        if self.need_knp is False:
            for base_phrase in self.base_phrases:
                if fstring := base_phrase.features.get("NE"):
                    assert isinstance(fstring, str)
                    candidate_morphemes = self.morphemes[: base_phrase.morphemes[-1].index + 1]
                    if named_entity := NamedEntity.from_fstring(fstring, candidate_morphemes):
                        self.named_entities.append(named_entity)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        return self._sent_id == other._sent_id and self.text == other.text

    @property
    def global_index(self) -> int:
        """文書全体におけるインデックス．"""
        return self.index

    @property
    def parent_unit(self) -> Optional["Document"]:
        """上位の言語単位（文書）．未登録なら None．"""
        return self._document

    @property
    def child_units(self) -> Optional[Union[List[Clause], List[Phrase], List[Morpheme]]]:
        """下位の言語単位（節もしくは形態素）のリスト．解析結果にアクセスできないなら None．

        .. note::
            KNP によって解析済みなら節， Jumanpp によって解析済みなら形態素のリストを返却．
            KNP による素性が付与されていない場合は節境界が判断できないため文節を返却．
        """
        if self._clauses is not None:
            return self._clauses
        elif self._phrases is not None:
            return self._phrases
        elif self._morphemes is not None:
            return self._morphemes
        return None

    @property
    def doc_id(self) -> str:
        """文書 ID．

        Raises:
            AttributeError: 文書 IDにアクセスできない場合．
        """
        if self._doc_id is None:
            raise AttributeError("doc_id has not been set")
        return self._doc_id

    @doc_id.setter
    def doc_id(self, doc_id: str) -> None:
        """文書 ID．

        Args:
            doc_id: 文書 ID．
        """
        self._doc_id = doc_id

    @property
    def did(self) -> str:
        """文書 ID（doc_id のエイリアス）．

        Raises:
            AttributeError: 文書 IDにアクセスできない場合．
        """
        return self.doc_id

    @did.setter
    def did(self, did: str) -> None:
        """文書 ID（doc_id のエイリアス）．

        Args:
            did: 文書 ID．
        """
        self.doc_id = did

    @property
    def sent_id(self) -> str:
        """文 ID．

        Raises:
            AttributeError: 文 IDにアクセスできない場合．
        """
        if self._sent_id is None:
            raise AttributeError("sid has not been set")
        return self._sent_id

    @sent_id.setter
    def sent_id(self, sid: str) -> None:
        """文 ID．

        Args:
            sid: 文 ID．
        """
        self._sent_id = sid

    @property
    def sid(self) -> str:
        """文 ID（sent_id のエイリアス）．

        Raises:
            AttributeError: 文 IDにアクセスできない場合．
        """
        return self.sent_id

    @sid.setter
    def sid(self, sid: str) -> None:
        """文 ID（sent_id のエイリアス）．

        Args:
            sid: 文 ID．
        """
        self.sent_id = sid

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._document is None:
            raise AttributeError("document has not been set")
        return self._document

    @document.setter
    def document(self, document: "Document") -> None:
        """文書．

        Args:
            document: 文書．
        """
        self._document = document

    @property
    def clauses(self) -> List[Clause]:
        """節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._clauses is None:
            raise AttributeError("clauses have not been set")
        return self._clauses

    @clauses.setter
    def clauses(self, clauses: List[Clause]) -> None:
        """節のリスト．

        Args:
            clauses: 節のリスト．
        """
        for clause in clauses:
            clause.sentence = self
        self._clauses = clauses

    @property
    def phrases(self) -> List[Phrase]:
        """文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._phrases is not None:
            return self._phrases
        if self._clauses is not None:
            return [phrase for clause in self.clauses for phrase in clause.phrases]
        raise AttributeError("phrases have not been set")

    @phrases.setter
    def phrases(self, phrases: List[Phrase]) -> None:
        """文節のリスト．

        Args:
            phrases: 文節のリスト．
        """
        for phrase in phrases:
            phrase.sentence = self
        self._phrases = phrases

    @property
    def base_phrases(self) -> List[BasePhrase]:
        """基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [base_phrase for phrase in self.phrases for base_phrase in phrase.base_phrases]

    @property
    def morphemes(self) -> List[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._clauses is not None:
            return [morpheme for clause in self.clauses for morpheme in clause.morphemes]
        if self._phrases is not None:
            return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]
        if self._morphemes is not None:
            return self._morphemes
        raise AttributeError("morphemes have not been set")

    @morphemes.setter
    def morphemes(self, morphemes: List[Morpheme]) -> None:
        """形態素のリスト．

        Args:
            morphemes: 形態素のリスト．
        """
        for morpheme in morphemes:
            morpheme.sentence = self
        self._morphemes = morphemes

    @property
    def comment(self) -> str:
        """コメント行．"""
        ret = ""
        if sid := self._sent_id:
            ret += f"S-ID:{sid} "
        if misc := self.misc_comment:
            ret += f"{misc} "
        if ret != "":
            ret = "# " + ret
        return ret.rstrip(" ")

    @comment.setter
    def comment(self, comment: str) -> None:
        """コメント行．

        Args:
            comment: コメント行．
        """
        doc_id, sid, rest = self._extract_sid(comment)
        if sid is not None:
            self.sid = sid
        if doc_id is not None:
            self.doc_id = doc_id
        self.misc_comment = rest

    @property
    def has_document(self) -> bool:
        """文書が設定されていたら True．"""
        return self._document is not None

    @property
    def need_jumanpp(self) -> bool:
        """Juman++ による形態素解析がまだなら True．"""
        return self._morphemes is None and self._phrases is None and self._clauses is None

    @property
    def need_knp(self) -> bool:
        """KNP による構文解析がまだなら True．"""
        return self._phrases is None and self._clauses is None

    @property
    def need_clause_tag(self) -> bool:
        """KNP による節-主辞・節-区切のタグ付与がまだなら True．"""
        return self._clauses is None

    @classmethod
    def from_raw_text(cls, text: str, post_init: bool = True) -> "Sentence":
        """文クラスのインスタンスを文の文字列から初期化．

        Args:
            text: 文の文字列．
            post_init: インスタンス作成後の追加処理を行うなら True．

        Example:
            >>> from rhoknp import Sentence
            >>> text = "天気が良かったので散歩した。"
            >>> sent = Sentence(text)
        """
        sentence = cls()
        text_lines = []
        for line in text.splitlines():
            if line.strip() == "":
                continue
            if cls.is_comment_line(line):
                sentence.comment = line
            else:
                text_lines.append(line)
        sentence.text = "".join(text_lines)
        if post_init is True:
            sentence.__post_init__()
        return sentence

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str, post_init: bool = True) -> "Sentence":
        """文クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．
            post_init: インスタンス作成後の追加処理を行うなら True．

        Raises:
            ValueError: 解析結果読み込み中にエラーが発生した場合．

        Example:
            >>> from rhoknp import Sentence
            >>> jumanpp_text = \"\"\"
            ... # S-ID:1
            ... 天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物"
            ... が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            ... 良かった よかった 良い 形容詞 3 * 0 イ形容詞アウオ段 18 タ形 8 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ... ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
            ... 散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
            ... した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
            ... 。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            ... EOS
            ... \"\"\"
            >>> sent = Sentence.from_jumanpp(jumanpp_text)
        """
        sentence = cls()
        morphemes: List[Morpheme] = []
        jumanpp_lines: List[str] = []
        for line in jumanpp_text.split("\n"):
            if line.strip() == "":
                continue
            if cls.is_comment_line(line):
                sentence.comment = line
                continue
            if Morpheme.is_morpheme_line(line):
                if jumanpp_lines:
                    morphemes.append(Morpheme.from_jumanpp("\n".join(jumanpp_lines)))
                    jumanpp_lines = []
                jumanpp_lines.append(line)
                continue
            if Morpheme.is_homograph_line(line):
                jumanpp_lines.append(line)
                continue
            if line.strip() == cls.EOS:
                if jumanpp_lines:
                    morphemes.append(Morpheme.from_jumanpp("\n".join(jumanpp_lines)))
                break
            raise ValueError(f"malformed line: {line}")
        sentence.morphemes = morphemes
        if post_init is True:
            sentence.__post_init__()
        return sentence

    @classmethod
    def from_knp(cls, knp_text: str, post_init: bool = True) -> "Sentence":
        """文クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
            post_init: インスタンス作成後の追加処理を行うなら True．

        Raises:
            ValueError: 解析結果読み込み中にエラーが発生した場合．

        Example:
            >>> from rhoknp import Sentence
            >>> knp_text = \"\"\"
            ... # S-ID:1
            ... * 1D
            ... + 1D
            ... 天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物"
            ... が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            ... * 2D
            ... + 2D <節-区切><節-主辞>
            ... 良かった よかった 良い 形容詞 3 * 0 イ形容詞アウオ段 18 タ形 8 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ... ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
            ... * -1D
            ... + -1D <節-区切><節-主辞>
            ... 散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
            ... した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
            ... 。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            ... EOS
            ... \"\"\"
            >>> sent = Sentence.from_knp(knp_text)
        """
        lines = knp_text.split("\n")
        sentence = cls()
        has_clause_boundary = any("節-区切" in line for line in lines if BasePhrase.is_base_phrase_line(line))
        clauses: List[Clause] = []
        phrases: List[Phrase] = []
        child_lines: List[str] = []
        is_clause_end = False
        for line in lines:
            if line.strip() == "":
                continue
            if cls.is_comment_line(line):
                sentence.comment = line
                continue
            if Phrase.is_phrase_line(line):
                if has_clause_boundary and is_clause_end and child_lines:
                    clauses.append(Clause.from_knp("\n".join(child_lines)))
                    child_lines = []
                    is_clause_end = False
                elif has_clause_boundary is False and child_lines:
                    phrases.append(Phrase.from_knp("\n".join(child_lines)))
                    child_lines = []
                child_lines.append(line)
                continue
            if BasePhrase.is_base_phrase_line(line):
                if "節-区切" in line:
                    is_clause_end = True
                child_lines.append(line)
                continue
            if Morpheme.is_morpheme_line(line) or Morpheme.is_homograph_line(line):
                child_lines.append(line)
                continue
            if line.strip() == cls.EOS:
                if has_clause_boundary:
                    clauses.append(Clause.from_knp("\n".join(child_lines)))
                else:
                    phrases.append(Phrase.from_knp("\n".join(child_lines)))
                break
            raise ValueError(f"malformed line: {line}")
        if has_clause_boundary is True:
            sentence.clauses = clauses
        else:
            sentence.phrases = phrases
        if post_init is True:
            sentence.__post_init__()
        return sentence

    @staticmethod
    def _extract_sid(comment: str) -> Tuple[Optional[str], Optional[str], str]:
        """Extract sentence id and document id from comment line.

        Args:
            comment: A comment line.

        Returns:
            Optional[str]: Document id if exists; otherwise, None.
            Optional[str]: Sentence id if exists; otherwise, None.
            str: The rest of the comment line.
        """
        assert comment.startswith("#")
        if match_sid := re.match(r"# S-ID: ?(\S*)( .+)?$", comment):
            sid_string = match_sid[1]
            match = (
                Sentence.SID_PAT_KWDLC.match(sid_string)
                or Sentence.SID_PAT_WAC.match(sid_string)
                or Sentence.SID_PAT.match(sid_string)
            )
            if match is None:
                raise ValueError(f"unsupported S-ID format: {sid_string}")
            return (
                match["did"],
                match["sid"],
                match_sid[2].lstrip() if match_sid[2] else "",
            )
        return None, None, comment.lstrip("#").lstrip(" ")

    def to_raw_text(self) -> str:
        """生テキストフォーマットに変換．"""
        ret = ""
        if self.comment != "":
            ret += self.comment + "\n"
        ret += self.text.rstrip("\n") + "\n"
        return ret

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        ret = ""
        if self.comment != "":
            ret += self.comment + "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + self.EOS + "\n"
        return ret

    def to_knp(self) -> str:
        """KNP フォーマットに変換．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        ret = ""
        if self.comment != "":
            ret += self.comment + "\n"
        ret += "".join(child.to_knp() for child in self._clauses or self.phrases)
        ret += self.EOS + "\n"
        return ret

    def reparse(self) -> "Sentence":
        """文を再構築．

        .. note::
            解析結果に対する編集を有効にする際に実行する必要がある．
        """
        if self.need_knp is False:
            return Sentence.from_knp(self.to_knp())
        elif self.need_jumanpp is False:
            return Sentence.from_jumanpp(self.to_jumanpp())
        return Sentence.from_raw_text(self.to_raw_text())

    @staticmethod
    def is_comment_line(line: str) -> bool:
        """コメント行なら True を返す．

        Args:
            line: 解析結果の一行．

        .. note::
            JUMAN/KNP では # から始まる行がコメントとみなされる．
        """
        return line.startswith("#") and not Morpheme.is_morpheme_line(line)
