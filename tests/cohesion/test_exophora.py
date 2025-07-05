from rhoknp.cohesion.exophora import ExophoraReferent, ExophoraReferentType


def test_exophora() -> None:
    referent = ExophoraReferent("著者")
    assert referent.type == ExophoraReferentType.WRITER
    assert referent.index is None
    assert str(referent) == "著者"
    assert repr(referent) == "ExophoraReferent(text='著者')"
    dup_referent = eval(repr(referent))
    unequal_referent = ExophoraReferent("読者")
    assert dup_referent == referent
    assert unequal_referent != referent
    assert hash(dup_referent) == hash(referent)
    assert hash(unequal_referent) != hash(referent)


def test_exophora_number() -> None:
    referent = ExophoraReferent("不特定:人３")
    assert referent.type == ExophoraReferentType.UNSPECIFIED_PERSON
    assert referent.index == 3
    assert str(referent) == "不特定:人3"
    assert repr(referent) == "ExophoraReferent(text='不特定:人3')"
    dup_referent = eval(repr(referent))
    unequal_referent = ExophoraReferent("不特定:人１")
    assert dup_referent == referent
    assert unequal_referent != referent
    assert hash(dup_referent) == hash(referent)
    assert hash(unequal_referent) != hash(referent)


def test_exophora_other() -> None:
    referent = ExophoraReferent("ほげほげ２")
    assert referent.type == ExophoraReferentType.OTHER
    assert referent.index is None
    assert str(referent) == "ほげほげ２"
    assert repr(referent) == "ExophoraReferent(text='ほげほげ２')"
    dup_referent = eval(repr(referent))
    unequal_referent = ExophoraReferent("前文")
    assert dup_referent == referent
    assert unequal_referent != referent
    assert hash(dup_referent) == hash(referent)
    assert hash(unequal_referent) != hash(referent)
