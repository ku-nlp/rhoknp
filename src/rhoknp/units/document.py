import logging
from collections.abc import Sequence
from typing import Optional, Union

try:
    from typing import override  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import override

from rhoknp.cohesion.pas import Pas
from rhoknp.props.named_entity import NamedEntity
from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.clause import Clause
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.phrase import Phrase
from rhoknp.units.sentence import Sentence
from rhoknp.units.unit import Unit
from rhoknp.utils.comment import is_comment_line

logger = logging.getLogger(__name__)


class Document(Unit):
    """文書クラス．

    Args:
        text: 文書の文字列．
    """

    EOD = "EOD"

    count = 0

    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__()

        Sentence.count = 0

        # child units
        self._sentences: Optional[list[Sentence]] = None

        if text is not None:
            self.text = text

        self.index = self.count
        Document.count += 1

        self.doc_id: str = ""  #: 文書 ID．

    @override
    def __post_init__(self) -> None:
        super().__post_init__()

        # Set doc_id.
        if not self.is_senter_required() and len(self.sentences) > 0:
            doc_ids = [sentence.doc_id for sentence in self.sentences]
            self.doc_id = doc_ids[0]
            if not all(doc_id == self.doc_id for doc_id in doc_ids):
                logger.warning(
                    f"'doc_id' is not consistent; use 'doc_id' extracted from the first sentence: {self.doc_id}."
                )

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Document):
            return False
        return self.doc_id == other.doc_id and self.text == other.text

    @property
    def parent_unit(self) -> None:
        """上位の言語単位．文書は最上位の言語単位なので常に None．"""
        return

    @property
    def child_units(self) -> Optional[list[Sentence]]:
        """下位の言語単位（文）のリスト．解析結果にアクセスできないなら None．"""
        return self._sentences

    @property
    def did(self) -> str:
        """文書 ID（doc_id のエイリアス）．"""
        return self.doc_id

    @did.setter
    def did(self, did: str) -> None:
        """文書 ID（doc_id のエイリアス）．

        Args:
            did: 文書 ID．
        """
        self.doc_id = did

    @property
    def sentences(self) -> list[Sentence]:
        """文のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._sentences is None:
            raise AttributeError("sentences have not been set")
        return self._sentences

    @sentences.setter
    def sentences(self, sentences: list[Sentence]) -> None:
        """文のリスト．

        Args:
            sentences: 文のリスト．
        """
        for sentence in sentences:
            sentence.document = self
        self._sentences = sentences

    @property
    def clauses(self) -> list[Clause]:
        """節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [clause for sentence in self.sentences for clause in sentence.clauses]

    @property
    def phrases(self) -> list[Phrase]:
        """文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [phrase for sentence in self.sentences for phrase in sentence.phrases]

    @property
    def base_phrases(self) -> list[BasePhrase]:
        """基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [base_phrase for sentence in self.sentences for base_phrase in sentence.base_phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [morpheme for sentence in self.sentences for morpheme in sentence.morphemes]

    @property
    def named_entities(self) -> list[NamedEntity]:
        """固有表現のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [ne for sentence in self.sentences for ne in sentence.named_entities]

    @property
    def pas_list(self) -> list[Pas]:
        """述語項構造のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [pas for sentence in self.sentences for pas in sentence.pas_list]

    @classmethod
    def from_raw_text(cls, text: str) -> "Document":
        """文書クラスのインスタンスを文書の生テキストから初期化．

        Args:
            text: 文書の生テキスト．

        Example:
            >>> from rhoknp import Document
            >>> text = "天気が良かったので散歩した。途中で先生に会った。"
            >>> doc = Document.from_raw_text(text)
        """
        document = cls(text.strip())
        document.__post_init__()
        return document

    @classmethod
    def from_line_by_line_text(cls, text: str) -> "Document":
        """文書クラスのインスタンスを一行一文形式のテキストから初期化．

        Args:
            text: 一行一文形式に整形された文書のテキスト．

        Example:
            >>> from rhoknp import Document
            >>> sents = \"\"\"
            ... # S-ID:1
            ... 天気が良かったので散歩した。
            ... # S-ID:2
            ... 途中で先生に会った。
            ... \"\"\"
            >>> doc = Document.from_line_by_line_text(sents)

        .. note::
            # から始まる行は直後の文に対するコメントとして認識される．
        """
        document = cls()
        sentences = []
        sentence_lines: list[str] = []
        for line in text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if is_comment_line(line):
                continue
            sentences.append(Sentence.from_raw_text("\n".join(sentence_lines), post_init=False))
            sentence_lines = []
        document.sentences = sentences
        document.__post_init__()
        return document

    @classmethod
    def from_sentences(cls, sentences: Sequence[Union[Sentence, str]]) -> "Document":
        """文書クラスのインスタンスを文のリストから初期化．

        Args:
            sentences: 文（文の文字列）のリスト．

        Example:
            >>> from rhoknp import Document
            >>> sents = ["天気が良かったので散歩した。", "途中で先生に会った。"]
            >>> doc = Document.from_sentences(sents)
        """
        document = cls()
        sentences_ = []
        for sentence in sentences:
            if isinstance(sentence, Sentence):
                if sentence.is_jumanpp_required():
                    sentences_.append(Sentence.from_raw_text(sentence.text, post_init=False))
                elif sentence.is_knp_required():
                    sentences_.append(Sentence.from_jumanpp(sentence.to_jumanpp(), post_init=False))
                else:
                    sentences_.append(Sentence.from_knp(sentence.to_knp(), post_init=False))
            else:
                sentences_.append(Sentence.from_raw_text(sentence.strip(), post_init=False))
        document.sentences = sentences_
        document.__post_init__()
        return document

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Document":
        """文書クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．

        Raises:
            ValueError: 解析結果読み込み中にエラーが発生した場合．

        Example:
            >>> from rhoknp import Document
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
            ... # S-ID:2
            ... 途中 とちゅう 途中 名詞 6 時相名詞 10 * 0 * 0 "代表表記:途中/とちゅう カテゴリ:抽象物 弱時相名詞 修飾（デ格）"
            ... で で で 助詞 9 格助詞 1 * 0 * 0 NIL
            ... 先生 せんせい 先生 名詞 6 普通名詞 1 * 0 * 0 "代表表記:先生/せんせい ドメイン:教育・学習 カテゴリ:人 人名末尾"
            ... に に に 助詞 9 格助詞 1 * 0 * 0 NIL
            ... 会った あった 会う 動詞 2 * 0 子音動詞ワ行 12 タ形 10 "代表表記:会う/あう 反義:動詞:分かれる/わかれる;動詞:別れる/わかれる"
            ... EOS
            ... \"\"\"
            >>> doc = Document.from_jumanpp(jumanpp_text)

        .. note::
            複数文の解析結果が含まれている場合，一つの文書として扱われる．
        """
        document = cls()
        sentences = []
        sentence_lines: list[str] = []
        for line in jumanpp_text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if line.strip() == Sentence.EOS:
                sentences.append(Sentence.from_jumanpp("\n".join(sentence_lines) + "\n", post_init=False))
                sentence_lines = []
        if sentence_lines:
            logger.warning(f"the last sentence does not end with EOS: {sentence_lines}")
            sentence_lines.append(Sentence.EOS)
            sentences.append(Sentence.from_jumanpp("\n".join(sentence_lines) + "\n", post_init=False))
        document.sentences = sentences
        document.__post_init__()
        return document

    @classmethod
    def from_knp(cls, knp_text: str) -> "Document":
        """文書クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．

        Raises:
            ValueError: 解析結果読み込み中にエラーが発生した場合．

        Example:
            >>> from rhoknp import Document
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
            ... # S-ID:2
            ... * 2D
            ... + 2D
            ... 途中 とちゅう 途中 名詞 6 時相名詞 10 * 0 * 0 "代表表記:途中/とちゅう カテゴリ:抽象物 弱時相名詞 修飾（デ格）"
            ... で で で 助詞 9 格助詞 1 * 0 * 0 NIL
            ... * 2D
            ... + 2D
            ... 先生 せんせい 先生 名詞 6 普通名詞 1 * 0 * 0 "代表表記:先生/せんせい ドメイン:教育・学習 カテゴリ:人 人名末尾"
            ... に に に 助詞 9 格助詞 1 * 0 * 0 NIL
            ... * -1D
            ... + -1D <節-区切><節-主辞>
            ... 会った あった 会う 動詞 2 * 0 子音動詞ワ行 12 タ形 10 "代表表記:会う/あう 反義:動詞:分かれる/わかれる;動詞:別れる/わかれる"
            ... 。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            ... EOS
            ... \"\"\"
            >>> doc = Document.from_knp(knp_text)

        .. note::
            複数文の解析結果が含まれている場合，一つの文書として扱われる．
        """
        document = cls()
        sentences = []
        sentence_lines: list[str] = []
        for line in knp_text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if line.strip() == Sentence.EOS:
                sentences.append(Sentence.from_knp("\n".join(sentence_lines) + "\n", post_init=False))
                sentence_lines = []
        if sentence_lines:
            logger.warning(f"the last sentence does not end with EOS: {sentence_lines}")
            sentence_lines.append(Sentence.EOS)
            sentences.append(Sentence.from_knp("\n".join(sentence_lines) + "\n", post_init=False))
        document.sentences = sentences
        document.__post_init__()
        return document

    def is_senter_required(self) -> bool:
        """文分割がまだなら True．"""
        return self._sentences is None

    def is_jumanpp_required(self) -> bool:
        """Juman++ による形態素解析がまだなら True．"""
        return self.is_senter_required() or any(sentence.is_jumanpp_required() for sentence in self.sentences)

    def is_knp_required(self) -> bool:
        """KNP による構文解析がまだなら True．"""
        return self.is_senter_required() or any(sentence.is_knp_required() for sentence in self.sentences)

    def is_clause_tag_required(self) -> bool:
        """KNP による節-主辞・節-区切のタグ付与がまだなら True．"""
        return self.is_senter_required() or any(sentence.is_clause_tag_required() for sentence in self.sentences)

    def reparse(self) -> "Document":
        """文書を再構築．

        .. note::
            解析結果に対する編集を有効にする際に実行する必要がある．
        """
        if not self.is_knp_required():
            return Document.from_knp(self.to_knp())
        if not self.is_jumanpp_required():
            return Document.from_jumanpp(self.to_jumanpp())
        if not self.is_senter_required():
            return Document.from_line_by_line_text(self.to_raw_text())
        return Document.from_raw_text(self.to_raw_text())

    def to_raw_text(self) -> str:
        """生テキストフォーマットに変換．

        .. note::
            文分割済みの場合は一行一文の形式で出力．
        """
        if self.is_senter_required():
            return self.text.rstrip() + "\n"
        return "".join(sentence.to_raw_text() for sentence in self.sentences)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return "".join(sentence.to_jumanpp() for sentence in self.sentences)

    def to_knp(self) -> str:
        """KNP フォーマットに変換．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return "".join(sentence.to_knp() for sentence in self.sentences)
