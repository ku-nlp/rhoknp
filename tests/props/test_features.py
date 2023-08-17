from dataclasses import astuple, dataclass
from typing import Dict, Union

import pytest

from rhoknp.props import FeatureDict


@dataclass(frozen=True)
class FeaturesTestCase:
    fstring: str
    features: Dict[str, Union[str, bool]]
    length: int


cases = [
    FeaturesTestCase(
        fstring="""<BGH:構文/こうぶん><文節内><係:文節内><文頭><体言><名詞項候補><先行詞候補><正規化代表表記:構文/こうぶん>""",
        features={
            "BGH": "構文/こうぶん",
            "文節内": True,
            "係": "文節内",
            "文頭": True,
            "体言": True,
            "名詞項候補": True,
            "先行詞候補": True,
            "正規化代表表記": "構文/こうぶん",
        },
        length=8,
    ),
    FeaturesTestCase(
        fstring="""<ALT-京都-きょうと-京都-6-4-0-0-"代表表記:京都/きょうと 地名:日本:府">""",
        features={
            'ALT-京都-きょうと-京都-6-4-0-0-"代表表記:京都/きょうと 地名:日本:府"': True,
        },
        length=1,
    ),
    FeaturesTestCase(
        fstring=r"""<NE:OPTIONAL:html\>タグ>""",
        features={
            "NE": r"OPTIONAL:html>タグ",
        },
        length=1,
    ),
]


cases_with_ignored_tag = [
    FeaturesTestCase(
        fstring="""<rel type="ノ" target="不特定:人"/><BGH:関心/かんしん><解析済><体言>""",
        features={
            "BGH": "関心/かんしん",
            "解析済": True,
            "体言": True,
        },
        length=3,
    ),
]


@pytest.mark.parametrize("fstring, features, length", [astuple(case) for case in cases + cases_with_ignored_tag])
def test_from_fstring(fstring: str, features: Dict[str, Union[str, bool]], length: int) -> None:
    fs = FeatureDict.from_fstring(fstring)
    assert len(fs) == length
    assert dict(fs) == features
    assert fs.get("dummy") is None


@pytest.mark.parametrize("fstring, features, length", [astuple(case) for case in cases])
def test_to_fstring(fstring: str, features: Dict[str, Union[str, bool]], length: int) -> None:
    fs = FeatureDict.from_fstring(fstring)
    assert fs.to_fstring() == fstring


def test_false():
    assert FeatureDict._item_to_fstring("sem", False) == ""


def test_ignore_tag_prefix():
    features = FeatureDict()
    features["rel"] = 'type="ノ" target="ユーザー" sid="w201106-0000060560-1" id="1"'
    assert len(features) == 0

    features["memo"] = 'text="メモ"'
    assert len(features) == 0


def test_modification():
    features = FeatureDict.from_fstring("""<用言:動><主節>""")
    assert features.to_fstring() == """<用言:動><主節>"""
    # Update
    features["用言"] = "判"
    assert features.to_fstring() == """<用言:判><主節>"""
    # Insert
    features["文末"] = True
    assert features.to_fstring() == """<用言:判><主節><文末>"""
    # Delete
    del features["主節"]
    assert features.to_fstring() == """<用言:判><文末>"""
