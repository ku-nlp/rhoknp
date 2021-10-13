from rhoknp.units.utils import RelMode, Rels

fstring = """<rel type="=≒" target="オフェンス" sid="w201106-0001519365-1" id="3"/><rel type="=≒" mode="AND" target="ディフェンス" sid="w201106-0001519365-1" id="4"/><rel type="ノ？" target="著者"/>"""


def test_rels_from_fstring() -> None:
    rels = Rels.from_fstring(fstring)
    assert len(rels) == 3

    rel = rels[0]
    assert rel.type == "=≒"
    assert rel.target == "オフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.phrase_index == 3
    assert rel.mode is None

    rel = rels[1]
    assert rel.type == "=≒"
    assert rel.target == "ディフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.phrase_index == 4
    assert rel.mode == RelMode.AND

    rel = rels[2]
    assert rel.type == "ノ？"
    assert rel.target == "著者"
    assert rel.sid is None
    assert rel.phrase_index is None
    assert rel.mode is None


def test_rels_to_fstring() -> None:
    rels = Rels.from_fstring(fstring)
    assert rels.to_fstring() == fstring
