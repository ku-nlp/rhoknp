import select
import threading
from collections.abc import Callable
from subprocess import Popen


def run_request(
    process: Popen[bytes],
    input_text: str,
    end_marker: str,
    timeout: int,
    log_stderr: Callable[[str], None],
    name: str,
) -> str:
    """Send one request and read both output streams until its end marker."""
    stdout_text = ""
    worker_error: Exception | None = None

    def worker() -> None:
        nonlocal stdout_text, worker_error
        try:
            assert process.stdin is not None
            input_bytes = memoryview(input_text.encode("utf-8"))
            while input_bytes:
                written = process.stdin.write(input_bytes)
                input_bytes = input_bytes[written:]
            stdout_text = _read_output(process, end_marker, log_stderr, name)
        except Exception as error:
            worker_error = error

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        process.kill()
        process.wait()
        thread.join()
        raise TimeoutError(f"Operation timed out after {timeout} seconds.")
    if worker_error is not None:
        raise worker_error
    if process.poll() is not None:
        raise RuntimeError(f"{name} exited unexpectedly.")
    return stdout_text


def _read_output(process: Popen[bytes], end_marker: str, log_stderr: Callable[[str], None], name: str) -> str:
    assert process.stdout is not None
    assert process.stderr is not None
    streams = [process.stdout, process.stderr]
    buffers = dict.fromkeys(streams, b"")
    stdout_lines: list[str] = []
    finished = False
    received_end_marker = False

    while streams:
        ready, _, _ = select.select(streams, [], [], 0 if finished else None)
        if not ready:
            break
        for stream in ready:
            chunk = stream.read(65536)
            if not chunk:
                streams.remove(stream)
                if stream is process.stdout:
                    finished = True
                continue
            lines = (buffers[stream] + chunk).split(b"\n")
            buffers[stream] = lines.pop()
            for raw_line in lines:
                line = raw_line.decode("utf-8")
                if stream is process.stderr:
                    if line.strip():
                        log_stderr(line)
                elif line.strip() == end_marker:
                    received_end_marker = True
                    finished = True
                    streams.remove(stream)
                    break
                else:
                    stdout_lines.append(line + "\n")

    if buffers[process.stderr].strip():
        log_stderr(buffers[process.stderr].decode("utf-8"))
    if not received_end_marker:
        raise RuntimeError(f"{name} exited unexpectedly before {end_marker}.")
    return "".join(stdout_lines)
