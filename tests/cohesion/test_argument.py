import textwrap

import pytest

from rhoknp.cohesion import ArgumentType, EndophoraArgument, ExophoraArgument, ExophoraReferent, Pas, Predicate
from rhoknp.units import BasePhrase


def test_endophora_argument() -> None:
    argument_base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
            + 4D
            彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
            は は は 助詞 9 副助詞 2 * 0 * 0
            """
        )
    )
    predicate_base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
            + -1D
            言う いう 言う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
            """
        )
    )
    arg_type = ArgumentType.OMISSION
    argument = EndophoraArgument(argument_base_phrase, arg_type=arg_type)
    pas = Pas(Predicate(predicate_base_phrase))
    argument.pas = pas
    assert argument.type == arg_type
    assert argument.optional is False
    assert argument.is_special is False
    assert argument.pas == pas
    assert argument.base_phrase == argument_base_phrase
    with pytest.raises(AssertionError):
        _ = argument.document
    with pytest.raises(AssertionError):
        _ = argument.sentence
    with pytest.raises(AssertionError):
        _ = argument.clause
    with pytest.raises(AssertionError):
        _ = argument.phrase

    assert repr(argument) == "<rhoknp.cohesion.argument.EndophoraArgument: '彼は'>"
    assert str(argument) == argument_base_phrase.text
    assert argument != "test"
    # TODO: consider whether this is expected behavior
    assert argument == EndophoraArgument(argument_base_phrase, arg_type=ArgumentType.EXOPHORA)


def test_exophora_argument() -> None:
    predicate_base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
            + -1D
            言う いう 言う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
            """
        )
    )
    pas = Pas(Predicate(predicate_base_phrase))
    exophora_referent = ExophoraReferent("不特定:人")
    argument = ExophoraArgument(exophora_referent, eid=3)
    argument.pas = pas
    assert argument.type == ArgumentType.EXOPHORA
    assert argument.optional is False
    assert argument.is_special is True
    assert argument.pas == pas
    assert argument.exophora_referent == exophora_referent
    assert argument.eid == 3
    assert repr(argument) == f"ExophoraArgument(exophora_referent={repr(exophora_referent)}, eid=3)"
    assert eval(repr(argument)) == argument
    assert str(argument) == "不特定:人"
    assert argument != "test"
    assert argument == ExophoraArgument(exophora_referent, eid=1)  # TODO: consider whether this is expected
