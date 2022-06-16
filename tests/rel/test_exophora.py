from rhoknp.rel.exophora import ExophoraReferent, ExophoraReferentType


def test_exophora():
    referent = ExophoraReferent("著者")
    assert referent.type == ExophoraReferentType.WRITER
    assert referent.index is None
    assert str(referent) == "著者"
    assert repr(referent) == "ExophoraReferent(text='著者')"


def test_exophora_number():
    referent = ExophoraReferent("不特定:人３")
    assert referent.type == ExophoraReferentType.UNSPECIFIED_PERSON
    assert referent.index == 3
    assert str(referent) == "不特定:人3"
    assert repr(referent) == "ExophoraReferent(text='不特定:人3')"


def test_exophora_other():
    referent = ExophoraReferent("ほげほげ２")
    assert referent.type == ExophoraReferentType.OTHER
    assert referent.index is None
    assert str(referent) == "ほげほげ２"
    assert repr(referent) == "ExophoraReferent(text='ほげほげ２')"
