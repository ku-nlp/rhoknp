import pytest

from rhoknp.cohesion import Predicate
from rhoknp.units import BasePhrase


def test_predicate() -> None:
    knp = """+ -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく><用言代表表記:行く/いく><節-区切><節-主辞><主題格:一人称優位><格関係0:ガ:彼><格関係3:ヘ:大学><格解析結果:行く/いく:動12:ガ/N/彼/0/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;ヘ/C/大学/3/0/1;時間/U/-/-/-/-><標準用言代表表記:行く/いく>
行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10 "代表表記:行く/いく ドメイン:交通 反義:動詞:帰る/かえる 付属動詞候補（タ系）" <代表表記:行く/いく><ドメイン:交通><反義:動詞:帰る/かえる><付属動詞候補（タ系）><正規化代表表記:行く/いく><移動動詞><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
"""
    phrase = BasePhrase.from_knp(knp)
    predicate = Predicate(phrase, cfid="行く/いく:動12")
    assert predicate.unit == phrase
    assert predicate.cfid == "行く/いく:動12"
    with pytest.raises(AssertionError):
        _ = predicate.sid
    with pytest.raises(AttributeError):
        _ = predicate.pas
    assert str(predicate) == "行った。"
    assert repr(predicate) == "<rhoknp.cohesion.predicate.Predicate: '行った。'>"
