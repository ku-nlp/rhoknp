from rhoknp.units.morpheme import Morpheme


def is_comment_line(line: str) -> bool:
    """コメント行なら True を返す．"""
    return line.startswith("#") and Morpheme.JUMANPP_PAT.match(line) is None


def is_homograph_line(line: str) -> bool:
    """同形行なら True を返す．"""
    return line.startswith("@") and Morpheme.JUMANPP_PAT.match(line) is None


def is_phrase_line(line: str) -> bool:
    """文節行なら True を返す．"""
    return line.startswith("*") and Morpheme.JUMANPP_PAT.match(line) is None


def is_base_phrase_line(line: str) -> bool:
    """基本句行なら True を返す．"""
    return line.startswith("+") and Morpheme.JUMANPP_PAT.match(line) is None
