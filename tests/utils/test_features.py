from dataclasses import astuple, dataclass
from typing import Union

import pytest

from rhoknp.units.utils import Features


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
    )
]


@pytest.mark.parametrize("fstring,features,length", [astuple(case) for case in cases])
def test_from_fstring(fstring: str, features: dict[str, Union[str, bool]], length: int) -> None:
    fs = Features.from_fstring(fstring)
    assert len(fs) == length
    assert dict(fs) == features
    assert fs.get("dummy") is None


@pytest.mark.parametrize("fstring,features,length", [astuple(case) for case in cases])
def test_to_fstring(fstring: str, features: dict[str, Union[str, bool]], length: int) -> None:
    fs = Features.from_fstring(fstring)
    assert fs.to_fstring() == fstring


def test_false():
    assert Features._item2tag_string("sem", False) == ""
