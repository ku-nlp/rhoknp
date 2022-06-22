from rhoknp.units.utils import Rel, RelMode

fstring = """<rel type="=≒" target="オフェンス" sid="w201106-0001519365-1" id="3"/><rel type="=≒" mode="AND" target="ディフェンス" sid="w201106-0001519365-1" id="4"/><rel type="ノ？" target="著者"/>"""


def test_rels_from_fstring() -> None:
    rels = []
    for match in Rel.PAT.finditer(fstring):
        rels.append(
            Rel(
                type=match["type"],
                target=match["target"],
                sid=match["sid"],
                base_phrase_index=int(match["id"]) if match["id"] else None,
                mode=RelMode(match["mode"]) if match["mode"] else None,
            )
        )
    assert len(rels) == 3

    rel = rels[0]
    assert rel.type == "=≒"
    assert rel.target == "オフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.base_phrase_index == 3
    assert rel.mode is None

    rel = rels[1]
    assert rel.type == "=≒"
    assert rel.target == "ディフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.base_phrase_index == 4
    assert rel.mode == RelMode.AND

    rel = rels[2]
    assert rel.type == "ノ？"
    assert rel.target == "著者"
    assert rel.sid is None
    assert rel.base_phrase_index is None
    assert rel.mode is None
