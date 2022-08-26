from enum import Enum


class RelMode(Enum):
    """同一の基本句に同一タイプの関係タグが複数付いている場合にそれらの関係を表す列挙体．

        * AND: 関係の対象が並列である．
            (例) 太郎と花子が学校から<帰った> (ガ格:太郎, ガ格:花子 [and])
        * OR: 「AかB」のように意味的に or である．
            (例) 私は田園調布か国立に<住みたい> (ガ格:私, ニ格:田園調布, ニ格:国立 [or])
        * AMBIGUOUS:いずれの解釈も妥当であり，文脈から判断ができない．
            (例) 高知県の橋本知事は…国籍条項を<撤廃する>方針を明らかにした (ガ格:高知県, ガ格:橋本知事 [？], ガ格:不特定:人 [？], ヲ格:条項, 外の関係:方針)

    Notes:
        target が「なし」の場合、同じタイプの関係タグが任意的要素であることを示す．
            (例) 太郎は一人で<立っていた> (ガ格:太郎, デ格:一人, デ格:なし [？])
    """

    AND = "AND"
    OR = "OR"
    AMBIGUOUS = "？"
