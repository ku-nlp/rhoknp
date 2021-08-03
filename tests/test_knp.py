from subprocess import PIPE, Popen

import pytest

# from rhoknp import parse

JMN = ["jumanpp"]
KNP = ["knp", "-tab"]


@pytest.mark.parametrize("text", ["外国人参政権"])
def test_knp(text: str):
    with Popen(JMN, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p_jmn:
        with Popen(KNP, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p_knp:
            out, _ = p_jmn.communicate(input=text)
            out, _ = p_knp.communicate(input=out)
    # doc = parse(text)
    # assert out == doc.to_knp()
