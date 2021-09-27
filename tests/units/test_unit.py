from rhoknp.units.unit import Unit


def test_processor_apply():
    unit = Unit(None)
    try:
        _ = unit.child_units
    except NotImplementedError:
        pass
    except Exception:
        raise Exception
