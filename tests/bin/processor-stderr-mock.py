import io
import os
import subprocess
import sys
import time
from pathlib import Path


def wait_for_file(path: Path) -> None:
    deadline = time.monotonic() + 10
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Timed out waiting for {path}")
        time.sleep(0.01)


if "--hold-pipes" in sys.argv:
    wait_for_file(Path(sys.argv[-1]) / "release-descendant")
    os.write(2, b"late descendant diagnostic\n")
    sys.exit(0)

for stream in (sys.stdin, sys.stdout, sys.stderr):
    assert isinstance(stream, io.TextIOWrapper)
    stream.reconfigure(encoding="utf-8")
control_dir = Path(sys.argv[sys.argv.index("--control-dir") + 1])
protocol = sys.argv[sys.argv.index("--test-protocol") + 1]


def output() -> None:
    data = "# S-ID:sample-0\n猫 ねこ 猫 名詞 6 普通名詞 1 * 0 * 0 NIL\nEOS\n".encode()
    if protocol == "knp":
        data = b"* -1D\n+ -1D\n" + data
    if protocol != "kwja":
        data = data.removesuffix(b"EOS\n")
    for byte in data:
        os.write(1, bytes([byte]))


if (control_dir / "startup-flood").exists():
    sys.stderr.write("x" * 1048576 + "\n")
    sys.stderr.flush()
if (control_dir / "close-stdin").exists():
    control_dir.joinpath("close-stdin").unlink()
    sys.stderr.write("fatal: cannot initialize\n")
    sys.stderr.flush()
    os.close(0)
    time.sleep(30)

if (control_dir / "startup-holder").exists():
    control_dir.joinpath("startup-holder").unlink()
    subprocess.Popen([sys.executable, __file__, "--hold-pipes", str(control_dir)])
    os.write(2, b"child spawned\n")
    time.sleep(30)

text = ""
for line in sys.stdin:
    if protocol == "kwja":
        if line.strip() != "EOD":
            text += line
            continue
        case = text.strip()
    elif protocol == "knp":
        if line.strip() != "EOS":
            text += line
            continue
        case = text.splitlines()[0].removeprefix("# ") if text else ""
    else:
        case = line.strip()
    end_marker = b"EOD" if protocol == "kwja" else b"EOS"
    if case == "skipped":
        os.write(2, b"WARNING: skipped\n\nERROR: no examples\n")
    elif case == "buffered":
        os.write(2, b"first\nsecond\nthird\n")
        output()
    elif case == "flood":
        for index in range(10000):
            sys.stderr.write(f"diagnostic {index:05d}: " + "x" * 80 + "\n")
        sys.stderr.flush()
        output()
    elif case == "large-output":
        os.write(1, b"# " + b"x" * 1048576 + b"\n")
        os.write(2, b"large stdout written\n")
        output()
    elif case == "fragmented":
        data = "日本語の警告\n".encode()
        os.write(2, data[:1])
        time.sleep(0.02)
        os.write(2, data[1:])
        output()
    elif case == "silent":
        output()
    elif case in {"fragmented-eod", "delayed-stderr"}:
        if case == "fragmented-eod":
            os.write(2, "日本語の警告\n".encode()[:1])
        output()
        os.write(1, end_marker + b"\n")
        wait_for_file(control_dir / "release-stderr")
        data = "日本語の警告\n".encode()
        os.write(2, data[1:] if case == "fragmented-eod" else data)
        text = ""
        continue
    elif case == "unterminated-eof":
        os.write(2, b"message without newline")
        os.close(2)
        output()
    elif case == "invalid-stderr":
        os.write(2, b"\xff\n")
        time.sleep(30)
    elif case == "descendant":
        subprocess.Popen([sys.executable, __file__, "--hold-pipes", str(control_dir)])
        os.write(2, b"child spawned\n")
        time.sleep(30)
    elif case == "raw-crlf":
        os.write(1, b"first\r\nsecond\r\nEOD\r\n")
        text = ""
        continue
    elif case == "invalid-utf8":
        os.write(1, b"\xff\n")
    elif case == "crash":
        os.write(2, b"fatal diagnostic\n")
        os._exit(2)
    elif case == "eof":
        os.write(2, b"stdout closed\n")
        os.close(1)
        time.sleep(30)
    elif case == "continuous-output":
        while True:
            os.write(1, b"pending\n" * 4096)
    elif case == "timeout":
        os.write(2, b"before timeout\n")
        time.sleep(30)
    elif case:
        sys.stderr.write(f"input length: {len(case)}\n")
        sys.stderr.flush()
        output()
    os.write(1, end_marker + b"\n")
    text = ""
