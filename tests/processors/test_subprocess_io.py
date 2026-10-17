import errno
import sys
import threading
from collections.abc import Iterator
from io import BytesIO
from unittest.mock import Mock

import pytest

from rhoknp.processors._subprocess import SubprocessIO


@pytest.fixture
def stdout_bytes() -> bytes:
    return b"response\nEOS\n"


@pytest.fixture
def process(stdout_bytes: bytes) -> Mock:
    process = Mock(stdin=BytesIO(), stdout=BytesIO(stdout_bytes), stderr=BytesIO())
    process.poll.return_value = None
    return process


@pytest.fixture
def subprocess_io(process: Mock) -> Iterator[SubprocessIO]:
    """Queue the response before requests so thread scheduling cannot change the test case."""
    io = SubprocessIO(process, "EOS", Mock(), "mock")
    io._stdout_reader.join(5)
    io._stderr_reader.join(5)
    assert not io._stdout_reader.is_alive()
    assert not io._stderr_reader.is_alive()
    try:
        yield io
    finally:
        io.close()
        process.stdin.close()


@pytest.mark.parametrize(
    "stdout_bytes",
    [
        pytest.param(b"first\r\nsecond\r\nEOS\r\n", id="crlf"),
        pytest.param(b"first\rsecond\rEOS\r", id="cr"),
        pytest.param(b"first\nsecond\nEOS", id="end-marker-without-final-newline"),
    ],
)
def test_request_normalizes_line_endings_and_removes_end_marker(subprocess_io: SubprocessIO) -> None:
    assert subprocess_io.request("", timeout=5) == "first\nsecond\n"


def test_request_writes_all_utf8_bytes_despite_partial_writes(
    subprocess_io: SubprocessIO, process: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    stream = process.stdin
    assert isinstance(stream, BytesIO)
    write = stream.write

    def write_part(data: memoryview) -> int:
        return write(data[:2])

    monkeypatch.setattr(stream, "write", write_part)
    assert subprocess_io.request("日本語の入力", timeout=5) == "response\n"
    assert stream.getvalue() == "日本語の入力".encode()


def test_request_times_out_if_writer_is_blocked_after_response(
    subprocess_io: SubprocessIO, process: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    release_writer = threading.Event()

    def blocked_write(data: memoryview) -> int:
        assert release_writer.wait(5)
        return len(data)

    monkeypatch.setattr(process.stdin, "write", blocked_write)
    try:
        with pytest.raises(TimeoutError, match="Operation timed out after 0 seconds"):
            subprocess_io.request("input", timeout=0)
    finally:
        release_writer.set()
        assert subprocess_io._writer is not None
        subprocess_io._writer.join(5)
    assert not subprocess_io._writer.is_alive()


def test_request_raises_write_error_even_if_response_is_ready(
    subprocess_io: SubprocessIO, process: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    error = BrokenPipeError(errno.EPIPE, "broken pipe")
    monkeypatch.setattr(process.stdin, "write", Mock(side_effect=error))
    with pytest.raises(BrokenPipeError) as exc_info:
        subprocess_io.request("input", timeout=5)
    assert exc_info.value is error


def test_request_rejects_response_from_exited_process(subprocess_io: SubprocessIO, process: Mock) -> None:
    process.poll.return_value = 0
    with pytest.raises(RuntimeError, match=r"mock exited unexpectedly\.$"):
        subprocess_io.request("", timeout=5)


def test_close_during_interpreter_shutdown_does_not_wait(
    subprocess_io: SubprocessIO, process: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "is_finalizing", lambda: True)
    join = Mock()
    for reader in (subprocess_io._stdout_reader, subprocess_io._stderr_reader):
        monkeypatch.setattr(reader, "join", join)
    subprocess_io.close()
    assert subprocess_io._closed.is_set()
    assert subprocess_io._stderr_stopped.is_set()
    process.kill.assert_called_once_with()
    process.wait.assert_not_called()
    join.assert_not_called()
