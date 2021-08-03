from subprocess import PIPE, Popen

import pytest

# from rhoknp import parse

JMN = ["jumanpp"]


@pytest.mark.parametrize("text", ["外国人参政権"])
def test_jumanpp(text: str):
    with Popen(JMN, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
        out, _ = p.communicate(input=text)
    # doc = parse(text)
    # assert out == doc.to_jumanpp()
