import os
import sys
import time

protocol = sys.argv[sys.argv.index("--test-protocol") + 1]


def output() -> None:
    data = "# S-ID:sample-0\n猫 ねこ 猫 名詞 6 普通名詞 1 * 0 * 0 NIL\nEOS\n".encode()
    if protocol == "knp":
        data = b"* -1D\n+ -1D\n" + data
    if protocol != "kwja":
        data = data.removesuffix(b"EOS\n")
    for byte in data:
        os.write(1, bytes([byte]))


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
    elif case == "fragmented":
        data = "日本語の警告\n".encode()
        os.write(2, data[:1])
        time.sleep(0.02)
        os.write(2, data[1:])
        output()
    elif case == "unterminated":
        os.write(2, b"message without newline")
    elif case == "invalid-utf8":
        os.write(1, b"\xff\n")
    elif case == "crash":
        os.write(2, b"fatal diagnostic\n")
        os._exit(2)
    elif case == "eof":
        os.write(2, b"stdout closed\n")
        os.close(1)
        time.sleep(30)
    elif case == "timeout":
        os.write(2, b"before timeout\n")
        time.sleep(30)
    elif case:
        sys.stderr.write(f"input length: {len(case)}\n")
        sys.stderr.flush()
        output()
    sys.stdout.write("EOD\n" if protocol == "kwja" else "EOS\n")
    sys.stdout.flush()
    text = ""
