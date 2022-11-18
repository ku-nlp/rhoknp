import textwrap
from typing import Dict

import pytest

from rhoknp import Clause, Document, Sentence

CASES = [
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:1
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * 2D
            + 2D <節-区切><節-主辞>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12
            * -1D
            + -1D <節-区切><節-主辞>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10
            。 。 。 特殊 1 句点 1 * 0 * 0
            EOS
            """
        ),
        "num": 2,
        "parent_ids": [1, -1],
        "children_ids": [[], [0]],
    },
    {
        "knp": textwrap.dedent(
            textwrap.dedent(
                """\
                # S-ID:1
                * 1D
                + 2D
                EOS EOS EOS 名詞 6 組織名 6 * 0 * 0
                は は は 助詞 9 副助詞 2 * 0 * 0
                * -1D
                + 2D
                特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1
                + -1D <節-区切><節-主辞>
                記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物"
                です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27
                。 。 。 特殊 1 句点 1 * 0 * 0
                EOS
                """
            )
        ),
        "num": 1,
        "parent_ids": [-1],
        "children_ids": [[]],
    },
    {
        "knp": textwrap.dedent(
            textwrap.dedent(
                """\
                # S-ID:1
                * 1D
                + 1D
                ご飯 ごはん ご飯 名詞 6 普通名詞 1 * 0 * 0
                を を を 助詞 9 格助詞 1 * 0 * 0
                * 2D
                + 2D <節-主辞>
                食べて たべて 食べる 動詞 2 * 0 母音動詞 1 タ系連用テ形 14
                いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2
                * 4D
                + 4D <節-区切>
                ところ ところ ところ 名詞 6 副詞的名詞 9 * 0 * 0
                に に に 助詞 9 格助詞 1 * 0 * 0
                * 4D
                + 4D
                彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
                が が が 助詞 9 格助詞 1 * 0 * 0
                * -1D
                + -1D <節-区切><節-主辞>
                来た 来た 来る 動詞 2 * 0 カ変動詞来 15 タ形 10
                EOS
                """
            )
        ),
        "num": 2,
        "parent_ids": [1, -1],
        "children_ids": [[], [0]],
    },
]


KNP_SNIPPETS = [
    {
        "knp": textwrap.dedent(
            """\
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * 2D
            + 2D <節-区切><節-主辞>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12
            """
        ),
        "text": "天気がいいので",
        "phrase_num": 2,
        "base_phrase_num": 2,
        "morpheme_num": 4,
        "head_text": "いいので",
        "end_text": "いいので",
        "is_adnominal": False,
        "is_sentential_complement": False,
    },
    {
        "knp": textwrap.dedent(
            """\
            * -1D
            + -1D <節-区切><節-主辞>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10
            。 。 。 特殊 1 句点 1 * 0 * 0
            """
        ),
        "text": "散歩した。",
        "phrase_num": 1,
        "base_phrase_num": 1,
        "morpheme_num": 3,
        "head_text": "散歩した。",
        "end_text": "散歩した。",
        "is_adnominal": False,
        "is_sentential_complement": False,
    },
    {
        "knp": textwrap.dedent(
            """\
            * 1D
            + 2D
            EOS EOS EOS 名詞 6 組織名 6 * 0 * 0
            は は は 助詞 9 副助詞 2 * 0 * 0
            * -1D
            + 2D
            特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1
            + -1D <節-区切><節-主辞>
            記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0
            です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27
            。 。 。 特殊 1 句点 1 * 0 * 0
            """
        ),
        "text": "EOSは特殊記号です。",
        "phrase_num": 2,
        "base_phrase_num": 3,
        "morpheme_num": 6,
        "head_text": "記号です。",
        "end_text": "記号です。",
        "is_adnominal": False,
        "is_sentential_complement": False,
    },
    {
        "knp": textwrap.dedent(
            """\
            * 1D
            + 1D <節-主辞>
            走った はしった 走る 動詞 2 * 0 子音動詞ラ行 10 タ形 10
            * -1D
            + -1D <節-区切>
            ところ ところ ところ 名詞 6 副詞的名詞 9 * 0 * 0
            で で で 助詞 9 格助詞 1 * 0 * 0
            """
        ),
        "text": "走ったところで",
        "phrase_num": 2,
        "base_phrase_num": 2,
        "morpheme_num": 3,
        "head_text": "走った",
        "end_text": "ところで",
        "is_adnominal": False,
        "is_sentential_complement": False,
    },
    {
        "knp": textwrap.dedent(
            """\
            * 1D
            + 1D
            私 わたし 私 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * 2D
            + 2D <節-区切:連体修飾><節-主辞>
            育てて そだてて 育てる 動詞 2 * 0 母音動詞 1 タ系連用テ形 14
            いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2
            """
        ),
        "text": "私が育てている",
        "phrase_num": 2,
        "base_phrase_num": 2,
        "morpheme_num": 4,
        "head_text": "育てている",
        "end_text": "育てている",
        "is_adnominal": True,
        "is_sentential_complement": False,
    },
    {
        "knp": textwrap.dedent(
            """\
            * 3D
            + 3D
            彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
            は は は 助詞 9 副助詞 2 * 0 * 0
            * 2D
            + 2D
            水泳 すいえい 水泳 名詞 6 サ変名詞 2 * 0 * 0
            を を を 助詞 9 格助詞 1 * 0 * 0
            * 3D
            + 3D <節-区切:補文><節-主辞>
            頑張って がんばって 頑張る 動詞 2 * 0 子音動詞ラ行 10 タ系連用テ形 14
            いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2
            と と と 助詞 9 格助詞 1 * 0 * 0
            """
        ),
        "text": "彼は水泳を頑張っていると",
        "phrase_num": 3,
        "base_phrase_num": 3,
        "morpheme_num": 7,
        "head_text": "頑張っていると",
        "end_text": "頑張っていると",
        "is_adnominal": False,
        "is_sentential_complement": True,
    },
]


@pytest.mark.parametrize("case", CASES)
def test_document(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    for clause in doc.clauses:
        assert clause.document == doc


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_document_error(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    for clause in sent.clauses:
        with pytest.raises(AttributeError):
            _ = clause.document


@pytest.mark.parametrize("case", CASES)
def test_sentence(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    for clause in sent.clauses:
        assert clause.sentence == sent


@pytest.mark.parametrize("case", CASES)
def test_num_document(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert len(doc.clauses) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_num_sentence(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert len(sent.clauses) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_parent_document(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert [clause.parent.index if clause.parent else -1 for clause in doc.clauses] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_parent_sentence(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert [clause.parent.index if clause.parent else -1 for clause in sent.clauses] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_document(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert [[child.index for child in clause.children] for clause in doc.clauses] == case["children_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_sentence(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert [[child.index for child in clause.children] for clause in sent.clauses] == case["children_ids"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_from_knp(case: Dict[str, str]) -> None:
    _ = Clause.from_knp(case["knp"])


def test_from_knp_error() -> None:
    knp = textwrap.dedent(
        """\
        * 1D
        + 2D
        EOS EOS EOS 名詞 6 組織名 6 * 0 * 0
        は は は 助詞 9 副助詞 2 * 0 * 0
        * -1D
        + 2D
        特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1
        + -1D <節-区切>
        記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0
        です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27
        。 。 。 特殊 1 句点 1 * 0 * 0
        """
    )
    with pytest.raises(ValueError):
        _ = Clause.from_knp(knp)


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_to_knp(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.to_knp() == case["knp"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_text(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.text == case["text"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_phrase_num(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert len(clause.phrases) == case["phrase_num"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_base_phrase_num(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert len(clause.base_phrases) == case["base_phrase_num"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_morpheme_num(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert len(clause.morphemes) == case["morpheme_num"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_head_text(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.head.text == case["head_text"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_end_text(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.end.text == case["end_text"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_is_adnominal(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.is_adnominal == case["is_adnominal"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_is_sentential_complement(case: Dict[str, str]) -> None:
    clause = Clause.from_knp(case["knp"])
    assert clause.is_sentential_complement == case["is_sentential_complement"]
