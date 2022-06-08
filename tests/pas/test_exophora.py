from rhoknp.pas.exophora import ExophoraReferent, ExophoraReferentType


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
    assert str(referent) == "不特定:人３"
    assert repr(referent) == "ExophoraReferent(text='不特定:人３')"
