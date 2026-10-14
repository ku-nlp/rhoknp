import io
import sys
import threading
import time
from collections.abc import Callable
from queue import Empty, Queue
from subprocess import Popen


class SubprocessIO:
    """Read a persistent process's pipes independently of request boundaries.

    Calls to request and close must be serialized by the owning processor.
    """

    def __init__(self, process: Popen[bytes], end_marker: str, log_stderr: Callable[[str], None], name: str) -> None:
        self._process = process
        self._end_marker = end_marker
        self._log_stderr = log_stderr
        self._name = name
        self._output: Queue[str | Exception] = Queue()
        self._closed = threading.Event()
        self._stderr_stopped = threading.Event()
        self._writer: threading.Thread | None = None
        self._stdout_reader = threading.Thread(target=self._read_stdout, daemon=True)
        self._stderr_reader = threading.Thread(target=self._read_stderr, daemon=True)
        self._stdout_reader.start()
        self._stderr_reader.start()

    def _read_stdout(self) -> None:
        assert self._process.stdout is not None
        lines: list[str] = []
        try:
            with io.TextIOWrapper(self._process.stdout, encoding="utf-8") as stream:
                for line in stream:
                    if self._closed.is_set():
                        break
                    if line.strip() == self._end_marker:
                        self._output.put("".join(lines))
                        lines.clear()
                    else:
                        lines.append(line)
        except Exception as error:
            self._output.put(error)
        finally:
            self._output.put(RuntimeError(f"{self._name} exited unexpectedly before {self._end_marker}."))

    def _read_stderr(self) -> None:
        assert self._process.stderr is not None
        try:
            with io.TextIOWrapper(self._process.stderr, encoding="utf-8") as stream:
                for line in stream:
                    if self._stderr_stopped.is_set():
                        break
                    if line.strip():
                        self._log_stderr(line.rstrip("\n"))
        except Exception as error:
            self._output.put(error)

    def request(self, input_text: str, timeout: int) -> str:
        """Write a request and return stdout preceding its end marker."""
        deadline = time.monotonic() + timeout
        writer_error: Exception | None = None

        def write_input() -> None:
            nonlocal writer_error
            assert self._process.stdin is not None
            try:
                remaining = memoryview(input_text.encode("utf-8"))
                while remaining:
                    written = self._process.stdin.write(remaining)
                    remaining = remaining[written:]
            except Exception as error:
                writer_error = error
                self._output.put(error)
            finally:
                if self._closed.is_set():
                    self._process.stdin.close()

        self._writer = threading.Thread(target=write_input, daemon=True)
        self._writer.start()
        try:
            output = self._output.get(timeout=max(0, deadline - time.monotonic()))
        except Empty:
            raise TimeoutError(f"Operation timed out after {timeout} seconds.") from None
        if isinstance(output, Exception):
            raise output

        self._writer.join(max(0, deadline - time.monotonic()))
        if self._writer.is_alive():
            raise TimeoutError(f"Operation timed out after {timeout} seconds.")
        if writer_error is not None:
            raise writer_error
        if self._process.poll() is not None:
            raise RuntimeError(f"{self._name} exited unexpectedly.")
        return output

    def close(self) -> None:
        """Kill the process and allow at most one second for pipe threads to finish."""
        if self._closed.is_set():
            return
        self._closed.set()
        deadline = time.monotonic() + 1
        self._process.kill()
        if sys.is_finalizing():
            self._stderr_stopped.set()
            return
        self._process.wait(timeout=max(0, deadline - time.monotonic()))
        for thread in (self._writer, self._stdout_reader, self._stderr_reader):
            if thread is not None:
                thread.join(max(0, deadline - time.monotonic()))
        self._stderr_stopped.set()
        # A descendant can keep a pipe open after the direct child exits.
        # Each reader closes its own stream to avoid blocking here on its I/O lock.
        if self._writer is None or not self._writer.is_alive():
            assert self._process.stdin is not None
            self._process.stdin.close()
