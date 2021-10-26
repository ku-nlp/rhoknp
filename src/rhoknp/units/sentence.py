import re
import weakref
from typing import TYPE_CHECKING, List, Optional, Union

from rhoknp.utils.draw_tree import draw_tree

from .chunk import Chunk
from .clause import Clause
from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit

if TYPE_CHECKING:
    from .document import Document


class Sentence(Unit):
    """文クラス．

    Args:
        text: 文の文字列．

    Example::

        from rhoknp import Sentence

        # 文の文字列
        sent_text = "天気が良かったので散歩した。"
        sent = Sentence(sent_text)
    """

    EOS = "EOS"
    count = 0

    def __init__(self, text: Optional[str] = None):
        super().__init__()
        if text is not None:
            self.text = text

        Clause.count = 0
        Chunk.count = 0
        Phrase.count = 0
        Morpheme.count = 0

        # parent unit
        self._document: Optional["Document"] = None

        # child units
        self._clauses: Optional[list[Clause]] = None
        self._chunks: Optional[list[Chunk]] = None
        self._morphemes: Optional[list[Morpheme]] = None

        self.sid: Optional[str] = None
        self.comment: Optional[str] = None

        self.index = self.count
        Sentence.count += 1

    @property
    def parent_unit(self) -> Optional["Document"]:
        """上位の言語単位（文書）．未登録なら None．"""
        return self._document

    @property
    def child_units(self) -> Optional[Union[list[Clause], list[Chunk], list[Morpheme]]]:
        """下位の言語単位（節もしくは形態素）のリスト．解析結果にアクセスできないなら None．

        .. note::
            KNP によって解析済みなら節， Jumanpp によって解析済みなら形態素のリストを返却．
            KNP による素性が付与されていない場合は節境界が判断できないため文節を返却．
        """
        if self._clauses is not None:
            return self._clauses
        elif self._chunks is not None:
            return self._chunks
        elif self._morphemes is not None:
            return self._morphemes
        return None

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self.parent_unit is None:
            raise AttributeError("document has not been set")
        return self.parent_unit

    @document.setter
    def document(self, document: "Document") -> None:
        """文書．

        Args:
            document: 文書．
        """
        self._document = document

    @property
    def clauses(self) -> list[Clause]:
        """節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._clauses is None:
            raise AttributeError("not available before applying KNP")
        return self._clauses

    @clauses.setter
    def clauses(self, clauses: list[Clause]) -> None:
        """節のリスト．

        Args:
            clauses: 節のリスト．
        """
        for clause in clauses:
            clause.sentence = weakref.proxy(self)
        self._clauses = clauses

    @property
    def chunks(self) -> list[Chunk]:
        """文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._chunks is not None:
            return self._chunks
        elif self._clauses is not None:
            return [chunk for clause in self.clauses for chunk in clause.chunks]
        raise AttributeError("not available before applying KNP")

    @chunks.setter
    def chunks(self, chunks: list[Chunk]) -> None:
        """文節のリスト．

        Args:
            chunks: 文節のリスト．
        """
        for chunk in chunks:
            chunk.sentence = weakref.proxy(self)
        self._chunks = chunks

    @property
    def phrases(self) -> list[Phrase]:
        """基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._morphemes is not None:
            return self._morphemes
        elif self._clauses is not None:
            return [
                morpheme for phrase in self.phrases for morpheme in phrase.morphemes
            ]
        raise AttributeError("not available before applying Jumanpp")

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]) -> None:
        """形態素のリスト．

        Args:
            morphemes: 形態素のリスト．
        """
        for morpheme in morphemes:
            morpheme.sentence = weakref.proxy(self)
        self._morphemes = morphemes

    @property
    def need_jumanpp(self) -> bool:
        """Juman++ による形態素解析がまだなら True．"""
        return (
            self._morphemes is None and self._chunks is None and self._clauses is None
        )

    @property
    def need_knp(self) -> bool:
        """KNP による構文解析がまだなら True．"""
        if self.need_jumanpp:
            return True
        return self._chunks is None and self._clauses is None

    @classmethod
    def from_string(cls, text: str) -> "Sentence":
        """文クラスのインスタンスを文の文字列から初期化．

        Args:
            text: 文の文字列．

        Example::

            from rhoknp import Sentence

            # 文の文字列
            sent_text = "天気が良かったので散歩した。"
            sent = Sentence(sent_text)
        """
        sentence = cls()
        text_lines = []
        for line in text.split("\n"):
            if line.startswith("#"):
                sentence.comment = line
                match = re.match(r"# S-ID: ?(\S*)( .+)?$", line)
                if match:
                    sentence.sid = match.group(1)
            else:
                text_lines.append(line)
        sentence.text = "\n".join(text_lines)
        return sentence

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Sentence":
        """文クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．

        Example::

            from rhoknp import Sentence

            # 文の文字列
            jumanpp_text = \"\"\"天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            良かった よかった 良い 形容詞 3 * 0 イ形容詞アウオ段 18 タ形 8 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            \"\"\"
            sent = Sentence.from_jumanpp(jumanpp_text)
        """
        sentence = cls()
        morphemes: List[Morpheme] = []
        jumanpp_lines: List[str] = []
        for line in jumanpp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("#"):
                sentence.comment = line
                match = re.match(r"# S-ID: ?(\S*)( .+)?$", line)
                if match:
                    sentence.sid = match.group(1)
                continue
            if line.startswith("@") and not line.startswith("@ @"):
                # homograph
                pass
            elif jumanpp_lines:
                morpheme = Morpheme.from_jumanpp("\n".join(jumanpp_lines))
                morphemes.append(morpheme)
                jumanpp_lines = []
            jumanpp_lines.append(line)
            if line.strip() == cls.EOS:
                break
        sentence.morphemes = morphemes
        return sentence

    @classmethod
    def from_knp(cls, knp_text: str) -> "Sentence":
        """文クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．

        Example::

            from rhoknp import Sentence

            # 文の文字列
            knp_text = \"\"\"# S-ID: 1
            * 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
            + 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 2D <BGH:良い/よい><時制:過去><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
            + 2D <BGH:良い/よい><時制:過去><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞>
            良かった よかった 良い 形容詞 3 * 0 イ形容詞アウオ段 18 タ形 8 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            * -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
            + -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            \"\"\"
            sent = Sentence.from_knp(knp_text)
        """
        lines = knp_text.split("\n")
        sentence = cls()
        has_clause_boundary = any(
            "節-区切" in line for line in lines if line.startswith("+")
        )
        clauses: list[Clause] = []
        chunks: list[Chunk] = []
        child_lines: list[str] = []
        is_clause_end = False
        for line in lines:
            if not line.strip():
                continue
            if line.startswith("#"):
                sentence.comment = line
                match = re.match(r"# S-ID: ?(\S*)( .+)?$", line)
                if match:
                    sentence.sid = match.group(1)
                continue
            if line.startswith(";;"):
                raise Exception(f"Error: {line}")
            if line.startswith("+") and "節-区切" in line:
                is_clause_end = True
            if line.strip() == cls.EOS:
                if has_clause_boundary is True:
                    clauses.append(Clause.from_knp("\n".join(child_lines)))
                else:
                    chunks.append(Chunk.from_knp("\n".join(child_lines)))
                break
            if line.startswith("*"):
                if is_clause_end is True:
                    clause = Clause.from_knp("\n".join(child_lines))
                    clauses.append(clause)
                    child_lines = []
                    is_clause_end = False
                elif has_clause_boundary is False and child_lines:
                    chunk = Chunk.from_knp("\n".join(child_lines))
                    chunks.append(chunk)
                    child_lines = []
            child_lines.append(line)
        if has_clause_boundary is True:
            sentence.clauses = clauses
        else:
            sentence.chunks = chunks
        return sentence

    def to_plain(self) -> str:
        """プレーンテキストフォーマットに変換．"""
        ret = ""
        if self.comment is not None:
            ret += self.comment + "\n"
        ret += self.text.rstrip("\n") + "\n"
        return ret

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        ret = ""
        if self.comment is not None:
            ret += self.comment + "\n"
        ret += (
            "".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
            + self.EOS
            + "\n"
        )
        return ret

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = ""
        if self.comment is not None:
            ret += self.comment + "\n"
        ret += "".join(child.to_knp() for child in self._clauses or self.chunks)
        ret += self.EOS + "\n"
        return ret

    def draw_phrase_tree(self, show_pos: bool = True) -> None:
        """構文木を表示．

        Args:
            show_pos: True なら品詞情報を含めて表示．
        """
        draw_tree(self.phrases, show_pos=show_pos)
