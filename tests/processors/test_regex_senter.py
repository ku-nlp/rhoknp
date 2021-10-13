import pytest

from rhoknp import RegexSenter


@pytest.mark.parametrize(
    "document, sentence_strings",
    [
        (
            "天気がいいので散歩した。",
            ["天気がいいので散歩した。"],
        ),
        (
            "天気がいいので散歩した。散歩の途中で先生に出会った。",
            ["天気がいいので散歩した。", "散歩の途中で先生に出会った。"],
        ),
        (
            "天気がいいので散歩した．散歩の途中で先生に出会った．",
            ["天気がいいので散歩した．", "散歩の途中で先生に出会った．"],
        ),
        (
            "天気がいいので散歩した\n散歩の途中で先生に出会った",
            ["天気がいいので散歩した", "散歩の途中で先生に出会った"],
        ),
        (
            "天気がいいので散歩した。散歩の途中で Michael に出会った。",
            ["天気がいいので散歩した。", "散歩の途中で Michael に出会った。"],
        ),
        (
            "今何時ですか？次の予定があるので失礼します。",
            ["今何時ですか？", "次の予定があるので失礼します。"],
        ),
        (
            "今何時ですか?次の予定があるので失礼します。",
            ["今何時ですか?", "次の予定があるので失礼します。"],
        ),
        (
            "今何時ですか！次の予定があるので失礼します。",
            ["今何時ですか！", "次の予定があるので失礼します。"],
        ),
        (
            "今何時ですか! 次の予定があるので失礼します。",
            ["今何時ですか!", "次の予定があるので失礼します。"],
        ),
        (
            "今何時ですか？？？次の予定があるので失礼します！！！",
            ["今何時ですか？？？", "次の予定があるので失礼します！！！"],
        ),
        (
            "お疲れ様です♪次の予定があるので失礼します。",
            ["お疲れ様です♪", "次の予定があるので失礼します。"],
        ),
        (
            "お疲れ様です★次の予定があるので失礼します。",
            ["お疲れ様です★", "次の予定があるので失礼します。"],
        ),
        (
            "お疲れ様です☆次の予定があるので失礼します。",
            ["お疲れ様です☆", "次の予定があるので失礼します。"],
        ),
        (
            "なるほど…これは難しい問題ですね。",
            ["なるほど…", "これは難しい問題ですね。"],
        ),
        (
            "テレビで「今年の夏は暑いので、熱中症に注意しましょう。」と言っていた。",
            ["テレビで「今年の夏は暑いので、熱中症に注意しましょう。」と言っていた。"],
        ),
        (
            "そんな（笑\n安心してください（笑",
            ["そんな（笑", "安心してください（笑"],
        ),
    ],
)
def test_apply_to_document(document: str, sentence_strings: list[str]) -> None:
    senter = RegexSenter()
    doc = senter.apply_to_document(document)
    for i, sentence in enumerate(doc.sentences):
        assert sentence.text == sentence_strings[i]


def test_apply_to_sentence() -> None:
    senter = RegexSenter()
    text = "天気がいいので散歩した。"
    sent = senter.apply_to_sentence(text)
    assert sent.text == text


def test_repr() -> None:
    senter = RegexSenter()
    assert repr(senter) == "RegexSenter()"
