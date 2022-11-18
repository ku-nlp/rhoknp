import textwrap

from rhoknp.cohesion import ArgumentType, EndophoraArgument, ExophoraArgument, ExophoraReferent
from rhoknp.units import BasePhrase


def test_endophora_argument() -> None:
    knp = textwrap.dedent(
        """\
        + 4D
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
        は は は 助詞 9 副助詞 2 * 0 * 0 NIL
        """
    )
    base_phrase = BasePhrase.from_knp(knp)
    arg_type = ArgumentType.OMISSION
    argument = EndophoraArgument(base_phrase, arg_type=arg_type)
    assert argument.unit == base_phrase
    # assert argument.document == base_phrase.document
    # assert argument.sentence == base_phrase.sentence
    # assert argument.clause == base_phrase.clause
    # assert argument.phrase == base_phrase.phrase
    assert repr(argument) == "<rhoknp.cohesion.argument.EndophoraArgument: '彼は'>"
    assert str(argument) == base_phrase.text
    assert argument != "test"
    # TODO: consider whether this is expected behavior
    assert argument == EndophoraArgument(base_phrase, arg_type=ArgumentType.EXOPHORA)


def test_exophora_argument() -> None:
    exophora_referent = ExophoraReferent("不特定:人")
    argument = ExophoraArgument(exophora_referent, eid=3)
    assert argument.exophora_referent == exophora_referent
    assert argument.eid == 3
    assert repr(argument) == f"ExophoraArgument(exophora_referent={repr(exophora_referent)}, eid=3)"
    assert eval(repr(argument)) == argument
    assert str(argument) == "不特定:人"
    assert argument != "test"
    assert argument == ExophoraArgument(exophora_referent, eid=1)  # TODO: consider whether this is expected
