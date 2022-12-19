import textwrap

import pytest

from rhoknp.cohesion import Pas, Predicate
from rhoknp.units import BasePhrase


def test_predicate() -> None:
    knp = textwrap.dedent(
        """\
        + -1D <格解析結果:行く/いく:動12:ガ/N/彼/0/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;ヘ/C/大学/3/0/1;時間/U/-/-/-/->
        行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        """
    )
    base_phrase = BasePhrase.from_knp(knp)
    predicate = Predicate(base_phrase, cfid="行く/いく:動12")
    pas = Pas(predicate)
    predicate.pas = pas
    assert predicate.base_phrase == base_phrase
    assert predicate.cfid == "行く/いく:動12"
    assert predicate.text == "行った。"
    with pytest.raises(AssertionError):
        _ = predicate.sid
    assert predicate.pas == pas
    assert str(predicate) == "行った。"
    assert repr(predicate) == "<rhoknp.cohesion.predicate.Predicate: '行った。'>"
