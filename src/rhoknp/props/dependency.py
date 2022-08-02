from enum import Enum


class DepType(Enum):
    """文節，基本句の係り受けタイプを表す列挙体．"""

    DEPENDENCY = "D"
    PARALLEL = "P"
    APPOSITION = "A"
    IMPERFECT_PARALLEL = "I"
