from dataclasses import astuple, dataclass
from typing import Union

import pytest

from rhoknp.props import FeatureDict


@dataclass(frozen=True)
class FeaturesTestCase:
    fstring: str
    features: dict[str, Union[str, bool]]
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
]

cases_with_ignored_tag = [
    FeaturesTestCase(
        fstring="""<rel type="ノ" target="ユーザー" sid="w201106-0000060560-1" id="1"/><BGH:関心/かんしん><解析済><体言>""",
        features={
            "BGH": "関心/かんしん",
            "解析済": True,
            "体言": True,
        },
        length=3,
    ),
    FeaturesTestCase(
        fstring="""<NE:DATE:平成２３年度><BGH:年度/ねんど><解析済><カウンタ:年度>""",
        features={
            "BGH": "年度/ねんど",
            "解析済": True,
            "カウンタ": "年度",
        },
        length=3,
    ),
]


@pytest.mark.parametrize("fstring,features,length", [astuple(case) for case in cases + cases_with_ignored_tag])
def test_from_fstring(fstring: str, features: dict[str, Union[str, bool]], length: int) -> None:
    fs = FeatureDict.from_fstring(fstring)
    assert len(fs) == length
    assert dict(fs) == features
    assert fs.get("dummy") is None


@pytest.mark.parametrize("fstring,features,length", [astuple(case) for case in cases])
def test_to_fstring(fstring: str, features: dict[str, Union[str, bool]], length: int) -> None:
    fs = FeatureDict.from_fstring(fstring)
    assert fs.to_fstring() == fstring


def test_false():
    assert FeatureDict._item_to_fstring("sem", False) == ""


def test_ignore_tag_prefix():
    features = FeatureDict()
    features["rel"] = 'type="ノ" target="ユーザー" sid="w201106-0000060560-1" id="1"'
    features["NE"] = "MONEY:100円"
    assert len(features) == 0
