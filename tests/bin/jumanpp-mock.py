import os
import sys
import time

for raw_line in sys.stdin.buffer:
    line = raw_line.decode().rstrip("\r\n")
    if line == "time consuming input":
        time.sleep(5)
    if line == "error causing input":
        os.write(2, "エラー1\nエラー2\n".encode())
        sys.exit(1)

    if line in {"knp time consuming input", "knp error causing input"}:
        os.write(1, f"# {line}\n".encode())

    os.write(
        1,
        """こんにちは こんにちは こんにちは 感動詞 12 * 0 * 0 * 0 "代表表記:こんにちは/こんにちは"
さようなら さようなら さようなら 感動詞 12 * 0 * 0 * 0 "代表表記:さようなら/さようなら"
EOS
""".encode(),
    )
