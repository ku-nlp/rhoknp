import pytest

from rhoknp.cohesion import Argument, ArgumentType, ExophoraReferent, SpecialArgument
from rhoknp.units import BasePhrase


def test_argument() -> None:
    knp = """+ 4D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><人称代名詞><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ><解析格:ガ>
彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0 "代表表記:彼/かれ カテゴリ:人 漢字読み:訓" <代表表記:彼/かれ><カテゴリ:人><漢字読み:訓><正規化代表表記:彼/かれ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
"""
    base_phrase = BasePhrase.from_knp(knp)
    argument = Argument(base_phrase, arg_type=ArgumentType.OMISSION)
    assert argument.unit == base_phrase
    # assert argument.document == base_phrase.document
    # assert argument.sentence == base_phrase.sentence
    # assert argument.clause == base_phrase.clause
    # assert argument.phrase == base_phrase.phrase
    assert repr(argument) == f"Argument(base_phrase={repr(base_phrase)}, arg_type={repr(ArgumentType.OMISSION)})"
    assert str(argument) == base_phrase.text
    assert argument != "test"
    assert argument == Argument(base_phrase, arg_type=ArgumentType.EXOPHORA)  # TODO: consider whether this is expected
    with pytest.raises(AttributeError):
        _ = argument.pas


def test_special_argument() -> None:
    exophora_referent = ExophoraReferent("不特定:人")
    argument = SpecialArgument(exophora_referent, eid=3)
    assert argument.exophora_referent == exophora_referent
    assert argument.eid == 3
    assert repr(argument) == "SpecialArgument(exophora_referent=ExophoraReferent(text='不特定:人'), eid=3)"
    assert str(argument) == "不特定:人"
    assert argument != "test"
    assert argument == SpecialArgument(exophora_referent, eid=1)  # TODO: consider whether this is expected
    with pytest.raises(AttributeError):
        _ = argument.pas
