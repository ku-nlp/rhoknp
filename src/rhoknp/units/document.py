import weakref
from typing import Optional, Sequence, Union

from rhoknp.pas.pas import Pas
from rhoknp.pas.predicate import Predicate
from rhoknp.utils.constants import ALL_CASES

from .chunk import Chunk
from .clause import Clause
from .morpheme import Morpheme
from .phrase import Phrase
from .sentence import Sentence
from .unit import Unit


class Document(Unit):
    """文書クラス．

    Args:
        text: 文書の文字列．

    Example::

        from rhoknp import Document

        # 文書の文字列
        doc_text = "天気が良かったので散歩した。途中で先生に会った。"
        doc = Document(doc_text)
    """

    count = 0

    def __init__(self, text: Optional[str] = None):
        super().__init__()

        Sentence.count = 0

        # child units
        self._sentences: Optional[list[Sentence]] = None

        if text is not None:
            self.text = text

        self.index = self.count
        Document.count += 1

        self._pass: dict[int, Pas] = {}
        if self.need_knp is False:
            self._parse_rel()

    @property
    def parent_unit(self) -> None:
        """上位の言語単位．文書は最上位の言語単位なので常に None．"""
        return None

    @property
    def child_units(self) -> Optional[list[Sentence]]:
        """下位の言語単位（文）のリスト．解析結果にアクセスできないなら None．"""
        return self._sentences

    @property
    def sentences(self) -> list[Sentence]:
        """文のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._sentences is None:
            raise AttributeError("not available before applying a sentence splitter")
        return self._sentences

    @sentences.setter
    def sentences(self, sentences: list[Sentence]) -> None:
        """文のリスト．

        Args:
            sentences: 文のリスト．
        """
        for sentence in sentences:
            sentence.document = weakref.proxy(self)
        self._sentences = sentences

    @property
    def clauses(self) -> list[Clause]:
        """節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [clause for sentence in self.sentences for clause in sentence.clauses]

    @property
    def chunks(self) -> list[Chunk]:
        """文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [chunk for clause in self.clauses for chunk in clause.chunks]

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
        return [
            morpheme for sentence in self.sentences for morpheme in sentence.morphemes
        ]

    @property
    def need_senter(self) -> bool:
        """文分割がまだなら True．"""
        return self._sentences is None

    @property
    def need_jumanpp(self) -> bool:
        """Juman++ による形態素解析がまだなら True．"""
        if self.need_senter:
            return True
        return any(sentence.need_jumanpp for sentence in self.sentences)

    @property
    def need_knp(self) -> bool:
        """KNP による構文解析がまだなら True．"""
        if self.need_senter:
            return True
        return any(sentence.need_knp for sentence in self.sentences)

    def pas_list(self) -> list[Pas]:
        return list(self._pass.values())

    @classmethod
    def from_string(cls, text: str) -> "Document":
        """文書クラスのインスタンスを文書の文字列から初期化．

        Args:
            text: 文書の文字列．

        Example::

            from rhoknp import Document

            # 文書の文字列
            doc_text = "天気が良かったので散歩した。途中で先生に会った。"
            doc = Document.from_string(doc_text)
        """
        return cls(text)

    @classmethod
    def from_sentence(cls, sentence: Union[Sentence, str]) -> "Document":
        """文書クラスのインスタンスを文から初期化．

        Args:
            sentence: 文もしくは文の文字列．

        Example::

            from rhoknp import Document

            # 文の文字列
            sent_text = "天気が良かったので散歩した。"
            doc = Document.from_sentence(sent_text)
        """
        document = cls()
        if isinstance(sentence, str):
            sentence = Sentence(sentence)
        document.sentences = [sentence]
        return document

    @classmethod
    def from_sentences(
        cls, sentences: Union[Sequence[Union[Sentence, str]], str]
    ) -> "Document":
        """文書クラスのインスタンスを文のリストから初期化．

        Args:
            sentences: 文（文の文字列）のリストもしくは一行一文形式の文字列．

        Example::

            from rhoknp import Document

            # 文（の文字列）のリスト
            sent_texts = ["天気が良かったので散歩した。", "途中で先生に会った。"]
            doc = Document.from_sentences(sent_texts)

            # 一行一文形式の文字列
            sent_texts = \"\"\"# S-ID: 1
            天気が良かったので散歩した。
            # S-ID: 2
            途中で先生に会った。
            \"\"\"
            doc = Document.from_sentences(sent_texts)

        .. note::
            一行一文形式の文字列を入力とするとき，# から始まる行はコメントとして認識される．
        """
        document = cls()
        sentences_ = []
        sentence_lines: list[str] = []
        if isinstance(sentences, str):
            sentences = sentences.split("\n")
        for sentence in sentences:
            if isinstance(sentence, str):
                sentence_lines.append(sentence)
                if sentence.startswith("# "):
                    continue
                sentence = Sentence.from_string("\n".join(sentence_lines))
                sentence_lines = []
            sentences_.append(sentence)
        document.sentences = sentences_
        return document

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Document":
        """文書クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．

        Example::

            from rhoknp import Document

            # Juman++ の解析結果
            jumanpp_text = \"\"\"天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            良かった よかった 良い 形容詞 3 * 0 イ形容詞アウオ段 18 タ形 8 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            途中 とちゅう 途中 名詞 6 時相名詞 10 * 0 * 0 "代表表記:途中/とちゅう カテゴリ:抽象物 弱時相名詞 修飾（デ格）"
            で で で 助詞 9 格助詞 1 * 0 * 0 NIL
            先生 せんせい 先生 名詞 6 普通名詞 1 * 0 * 0 "代表表記:先生/せんせい ドメイン:教育・学習 カテゴリ:人 人名末尾"
            に に に 助詞 9 格助詞 1 * 0 * 0 NIL
            会った あった 会う 動詞 2 * 0 子音動詞ワ行 12 タ形 10 "代表表記:会う/あう 反義:動詞:分かれる/わかれる;動詞:別れる/わかれる"
            EOS
            \"\"\"
            doc = Document.from_jumanpp(jumanpp_text)

        .. note::
            複数文の解析結果が含まれている場合，一つの文書として扱われる．．
        """
        document = cls()
        sentences = []
        sentence_lines: list[str] = []
        for line in jumanpp_text.split("\n"):
            if line.strip() == "":
                continue
            sentence_lines.append(line)
            if line.strip() == Sentence.EOS:
                sentences.append(
                    Sentence.from_jumanpp("\n".join(sentence_lines) + "\n")
                )
                sentence_lines = []
        document.sentences = sentences
        return document

    @classmethod
    def from_knp(cls, knp_text: str) -> "Document":
        """文書クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．

        Example::

            from rhoknp import Document

            # KNP の解析結果
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
            # S-ID: 2
            * 2D <SM-動作><BGH:途中/とちゅう><文頭><時間><デ><助詞><体言><修飾><係:デ格><区切:0-0><格要素><連用要素><正規化代表表記:途中/とちゅう><主辞代表表記:途中/とちゅう>
            + 2D <SM-動作><BGH:途中/とちゅう><文頭><時間><デ><助詞><体言><修飾><係:デ格><区切:0-0><格要素><連用要素><名詞項候補><正規化代表表記:途中/とちゅう><主辞代表表記:途中/とちゅう>
            途中 とちゅう 途中 名詞 6 時相名詞 10 * 0 * 0 "代表表記:途中/とちゅう カテゴリ:抽象物 弱時相名詞 修飾（デ格）" <代表表記:途中/とちゅう><カテゴリ:抽象物><弱時相名詞><修飾（デ格）><正規化代表表記:途中/とちゅう><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            で で で 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 2D <SM-主体><SM-人><BGH:先生/せんせい><ニ><助詞><体言><係:ニ格><区切:0-0><格要素><連用要素><正規化代表表記:先生/せんせい><主辞代表表記:先生/せんせい>
            + 2D <SM-主体><SM-人><BGH:先生/せんせい><ニ><助詞><体言><係:ニ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:先生/せんせい><主辞代表表記:先生/せんせい>
            先生 せんせい 先生 名詞 6 普通名詞 1 * 0 * 0 "代表表記:先生/せんせい ドメイン:教育・学習 カテゴリ:人 人名末尾" <代表表記:先生/せんせい><ドメイン:教育・学習><カテゴリ:人><人名末尾><正規化代表表記:先生/せんせい><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
            に に に 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * -1D <BGH:会う/あう><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:会う/あう><主辞代表表記:会う/あう>
            + -1D <BGH:会う/あう><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:会う/あう><主辞代表表記:会う/あう><用言代表表記:会う/あう><節-区切><節-主辞><主題格:一人称優位>
            会った あった 会う 動詞 2 * 0 子音動詞ワ行 12 タ形 10 "代表表記:会う/あう 反義:動詞:分かれる/わかれる;動詞:別れる/わかれる" <代表表記:会う/あう><反義:動詞:分かれる/わかれる;動詞:別れる/わかれる><正規化代表表記:会う/あう><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            \"\"\"
            doc = Document.from_knp(knp_text)

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
                sentences.append(Sentence.from_knp("\n".join(sentence_lines) + "\n"))
                sentence_lines = []
        document.sentences = sentences
        return document

    def to_plain(self) -> str:
        """プレーンテキストフォーマットに変換．

        .. note::
            文分割済みの場合は一行一文の形式で出力．
        """
        if self.need_senter:
            return self.text.rstrip() + "\n"
        return "".join(sentence.to_plain() for sentence in self.sentences)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        return "".join(sentence.to_jumanpp() for sentence in self.sentences)

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        return "".join(sentence.to_knp() for sentence in self.sentences)

    def _parse_rel(self) -> None:
        for phrase in self.phrases:
            assert phrase.index is not None
            pas = Pas(Predicate(phrase))
            for rel in phrase.rels:
                if rel.type not in ALL_CASES:
                    continue
                if rel.sid is not None:
                    sentence = next(
                        sent
                        for sent in phrase.document.sentences
                        if sent.sid == rel.sid
                    )
                    assert rel.phrase_index is not None
                    arg_phrase = sentence.phrases[rel.phrase_index]
                    assert rel.target in arg_phrase.text
                    pas.add_argument(rel.type, arg_phrase, mode=rel.mode)
                else:
                    pas.add_special_argument(
                        rel.type, rel.target, phrase.index, mode=rel.mode
                    )  # TODO: fix eid
            self._pass[phrase.index] = pas
