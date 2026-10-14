import errno
import logging
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import pytest

from rhoknp import KNP, KWJA, Jumanpp, Sentence


@pytest.fixture(params=["knp", "jumanpp", "kwja"])
def analyzer(
    request: pytest.FixtureRequest, caplog: pytest.LogCaptureFixture, tmp_path: Path
) -> Iterator[KNP | Jumanpp | KWJA]:
    options = [
        str(Path(__file__).parents[1] / "bin" / "processor-stderr-mock.py"),
        "--test-protocol",
        request.param,
        "--control-dir",
        str(tmp_path),
    ]
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
        assert processor._io is not None
        processor._io.close()


def wait_for_messages(caplog: pytest.LogCaptureFixture, messages: list[str]) -> None:
    deadline = time.monotonic() + 5
    while len(caplog.messages) < len(messages) and time.monotonic() < deadline:
        time.sleep(0.01)
    assert caplog.messages == messages


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
        pytest.param("large-output", ["large stdout written"], id="large-output"),
    ],
)
def test_diagnostics(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, case: str, messages: list[str]
) -> None:
    for _ in range(2):
        assert apply_case(analyzer, case, timeout=5) == "猫"
        wait_for_messages(caplog, messages)
        level = logging.WARNING if isinstance(analyzer, KWJA) else logging.DEBUG
        assert all(record.levelno == level for record in caplog.records)
        caplog.clear()


def test_diagnostics_with_only_end_marker(analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture) -> None:
    for _ in range(10):
        if isinstance(analyzer, KWJA):
            assert apply_case(analyzer, "skipped", timeout=5) == ""
        else:
            with pytest.raises(RuntimeError, match="returned empty result"):
                apply_case(analyzer, "skipped", timeout=5)
        wait_for_messages(caplog, ["WARNING: skipped", "ERROR: no examples"])
        caplog.clear()
        assert apply_case(analyzer, "buffered", timeout=5) == "猫"
        wait_for_messages(caplog, ["first", "second", "third"])
        caplog.clear()


@pytest.mark.parametrize(("case", "message"), [("crash", "fatal diagnostic"), ("eof", "stdout closed")])
def test_unexpected_eof(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, case: str, message: str
) -> None:
    with pytest.raises(RuntimeError, match=r"before EO[SD]"):
        apply_case(analyzer, case, timeout=5)
    wait_for_messages(caplog, [message])
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    wait_for_messages(caplog, ["first", "second", "third"])


def test_timeout(analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture) -> None:
    old_process = analyzer._proc
    assert old_process is not None
    with pytest.raises(TimeoutError):
        apply_case(analyzer, "timeout", timeout=1)
    assert old_process.poll() is not None
    wait_for_messages(caplog, ["before timeout"])
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    wait_for_messages(caplog, ["first", "second", "third"])


@pytest.mark.parametrize("case", ["invalid-utf8", "invalid-stderr"])
def test_worker_exception(analyzer: KNP | Jumanpp | KWJA, case: str) -> None:
    with pytest.raises(UnicodeDecodeError):
        apply_case(analyzer, case, timeout=5)
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"


@pytest.mark.parametrize("case", ["fragmented-eod", "delayed-stderr"])
def test_stderr_after_response(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, tmp_path: Path, case: str
) -> None:
    try:
        assert apply_case(analyzer, case, timeout=5) == "猫"
    finally:
        tmp_path.joinpath("release-stderr").touch()
    wait_for_messages(caplog, ["日本語の警告"])
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    wait_for_messages(caplog, ["first", "second", "third"])


def test_unterminated_stderr_at_eof(analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture) -> None:
    assert apply_case(analyzer, "unterminated-eof", timeout=5) == "猫"
    wait_for_messages(caplog, ["message without newline"])
    assert apply_case(analyzer, "silent", timeout=5) == "猫"


def test_stderr_during_input(analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    tmp_path.joinpath("startup-flood").touch()
    analyzer.start_process(skip_sanity_check=True)
    assert apply_case(analyzer, "あ" * 100000, timeout=5) == "猫"
    wait_for_messages(caplog, ["x" * 1048576, "input length: 100000"])


def test_broken_pipe_diagnostics(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, tmp_path: Path
) -> None:
    tmp_path.joinpath("close-stdin").touch()
    analyzer.start_process(skip_sanity_check=True)
    with pytest.raises(OSError, match=r"\[Errno ") as exc_info:
        apply_case(analyzer, "あ" * 100000, timeout=5)
    assert exc_info.value.errno in {errno.EPIPE, errno.EINVAL}
    assert "fatal: cannot initialize" in caplog.messages
    caplog.clear()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"
    wait_for_messages(caplog, ["first", "second", "third"])


@pytest.mark.parametrize("operation", ["read", "write"])
def test_timeout_with_inherited_pipes(
    analyzer: KNP | Jumanpp | KWJA, caplog: pytest.LogCaptureFixture, tmp_path: Path, operation: str
) -> None:
    if operation == "write":
        tmp_path.joinpath("startup-holder").touch()
        analyzer.start_process(skip_sanity_check=True)
    old_io = analyzer._io
    assert old_io is not None
    started = time.monotonic()
    try:
        with pytest.raises(TimeoutError):
            apply_case(analyzer, "descendant" if operation == "read" else "あ" * 100000, timeout=1)
        assert time.monotonic() - started < 4
        wait_for_messages(caplog, ["child spawned"])
        caplog.clear()
        assert apply_case(analyzer, "buffered", timeout=5) == "猫"
        wait_for_messages(caplog, ["first", "second", "third"])
    finally:
        tmp_path.joinpath("release-descendant").touch()
        old_io._stdout_reader.join(5)
        old_io._stderr_reader.join(5)
        assert old_io._writer is not None
        old_io._writer.join(5)
    assert not old_io._writer.is_alive()
    assert caplog.messages == ["first", "second", "third"]
    assert not old_io._stdout_reader.is_alive()
    assert not old_io._stderr_reader.is_alive()


@pytest.mark.parametrize("case", ["crlf", "cr", "no-final-newline"])
def test_output_line_endings(analyzer: KNP | Jumanpp | KWJA, case: str) -> None:
    assert apply_case(analyzer, case, timeout=5) == "猫"


def test_raw_crlf(tmp_path: Path) -> None:
    processor = KWJA(
        executable=sys.executable,
        options=[
            str(Path(__file__).parents[1] / "bin" / "processor-stderr-mock.py"),
            "--test-protocol",
            "kwja",
            "--control-dir",
            str(tmp_path),
            "--tasks",
            "typo",
        ],
    )
    try:
        assert processor.apply_to_document("raw-crlf").text == "first\nsecond"
    finally:
        assert processor._io is not None
        processor._io.close()


def test_restart_closes_pipes(analyzer: KNP | Jumanpp | KWJA) -> None:
    old_process = analyzer._proc
    old_io = analyzer._io
    assert old_process is not None
    assert old_io is not None
    analyzer.start_process(skip_sanity_check=True)
    assert old_process.poll() is not None
    for stream in (old_process.stdin, old_process.stdout, old_process.stderr):
        assert stream is not None
        assert stream.closed
    assert not old_io._stdout_reader.is_alive()
    assert not old_io._stderr_reader.is_alive()
    assert apply_case(analyzer, "buffered", timeout=5) == "猫"


def test_interpreter_shutdown(tmp_path: Path) -> None:
    code = (
        "import sys; from rhoknp import KWJA; "
        "processor = KWJA(executable=sys.executable, options=sys.argv[1:]); "
        "assert processor.apply_to_document('silent').text == '猫'"
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(Path(__file__).parents[1] / "bin" / "processor-stderr-mock.py"),
            "--test-protocol",
            "kwja",
            "--control-dir",
            str(tmp_path),
            "--tasks",
            "seq2seq",
        ],
        capture_output=True,
        encoding="utf-8",
        timeout=10,
        check=True,
    )
    assert result.stderr == ""


def test_timeout_with_continuous_output(analyzer: KNP | Jumanpp | KWJA) -> None:
    started = time.monotonic()
    with pytest.raises(TimeoutError):
        apply_case(analyzer, "continuous-output", timeout=1)
    assert time.monotonic() - started < 4
    assert apply_case(analyzer, "silent", timeout=5) == "猫"


def test_partial_writes(analyzer: KNP | Jumanpp | KWJA, monkeypatch: pytest.MonkeyPatch) -> None:
    assert analyzer._proc is not None
    assert analyzer._proc.stdin is not None
    write = analyzer._proc.stdin.write

    def write_part(data: memoryview) -> int | None:
        return write(data[:2])

    monkeypatch.setattr(analyzer._proc.stdin, "write", write_part)
    assert apply_case(analyzer, "partial-input", timeout=5) == "猫"
