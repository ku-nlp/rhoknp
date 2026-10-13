import logging
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from rhoknp import KNP, KWJA, Jumanpp, Sentence


@pytest.fixture(params=["knp", "jumanpp", "kwja"])
def analyzer(request: pytest.FixtureRequest, caplog: pytest.LogCaptureFixture) -> Iterator[KNP | Jumanpp | KWJA]:
    options = [str(Path(__file__).parents[1] / "bin" / "processor-stderr-mock.py"), "--test-protocol", request.param]
    processor: KNP | Jumanpp | KWJA
    if request.param == "knp":
        processor = KNP(executable=sys.executable, options=[*options, "-tab"])
    elif request.param == "jumanpp":
        processor = Jumanpp(executable=sys.executable, options=options)
    else:
        processor = KWJA(executable=sys.executable, options=[*options, "--tasks", "seq2seq"])
    caplog.set_level(logging.DEBUG, logger=type(processor).__module__)
    try:
        yield processor
    finally:
        assert processor._proc is not None
        processor._proc.kill()
        processor._proc.wait()


def apply_case(analyzer: KNP | Jumanpp | KWJA, case: str, timeout: int) -> str:
    if isinstance(analyzer, KNP):
        sentence = Sentence.from_jumanpp(f"# {case}\n猫 ねこ 猫 名詞 6 普通名詞 1 * 0 * 0 NIL\nEOS\n")
        return analyzer.apply_to_sentence(sentence, timeout=timeout).text
    if isinstance(analyzer, Jumanpp):
        return analyzer.apply_to_sentence(case, timeout=timeout).text
    return analyzer.apply_to_document(case, timeout=timeout).text


@pytest.mark.parametrize(
    ("case", "messages"),
    [
        pytest.param("buffered", ["first", "second", "third"], id="buffered-lines"),
        pytest.param("fragmented", ["日本語の警告"], id="split-utf8"),
        pytest.param(
            "flood", [f"diagnostic {index:05d}: " + "x" * 80 for index in range(10000)], id="larger-than-pipe"
        ),
        pytest.param("あ" * 100000, ["input length: 100000"], id="large-input"),
    ],
)
def test_diagnostics(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, case: str, messages: list[str]
) -> None:
    for _ in range(2):
        assert apply_case(analyzer, case, timeout=5) == "猫"
        assert caplog.messages == messages
        level = logging.WARNING if isinstance(analyzer, KWJA) else logging.DEBUG
        assert all(record.levelno == level for record in caplog.records)
        caplog.clear()


@pytest.mark.parametrize(
    ("case", "messages"),
    [("skipped", ["WARNING: skipped", "ERROR: no examples"]), ("unterminated", ["message without newline"])],
)
def test_diagnostics_with_only_end_marker(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, case: str, messages: list[str]
) -> None:
    for _ in range(10):
        if isinstance(analyzer, KWJA):
            assert apply_case(analyzer, case, timeout=5) == ""
        else:
            with pytest.raises(RuntimeError, match="returned empty result"):
                apply_case(analyzer, case, timeout=5)
        assert caplog.messages == messages
        caplog.clear()
        assert apply_case(analyzer, "buffered", timeout=5) == "猫"
        assert caplog.messages == ["first", "second", "third"]
        caplog.clear()


@pytest.mark.parametrize(("case", "message"), [("crash", "fatal diagnostic"), ("eof", "stdout closed")])
def test_unexpected_eof(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, case: str, message: str
) -> None:
    with pytest.raises(RuntimeError, match=r"before EO[SD]"):
        apply_case(analyzer, case, timeout=5)
    assert caplog.messages == [message]
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    assert caplog.messages == ["first", "second", "third"]


def test_timeout(analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture) -> None:
    old_process = analyzer._proc
    assert old_process is not None
    with pytest.raises(TimeoutError):
        apply_case(analyzer, "timeout", timeout=1)
    assert old_process.poll() is not None
    assert caplog.messages == ["before timeout"]
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    assert caplog.messages == ["first", "second", "third"]


def test_worker_exception(analyzer: KNP | Jumanpp | KWJA) -> None:
    with pytest.raises(UnicodeDecodeError):
        apply_case(analyzer, "invalid-utf8", timeout=5)
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
