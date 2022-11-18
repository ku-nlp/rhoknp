import re
import sys
from typing import TYPE_CHECKING, Sequence, TextIO, Union

from rhoknp.props.dependency import DepType

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase
    from rhoknp.units.phrase import Phrase

POS_MARK = {
    "特殊": "*",
    "動詞": "v",
    "形容詞": "j",
    "判定詞": "c",
    "助動詞": "x",
    "名詞": "n",
    "固有名詞": "N",
    "人名": "J",
    "地名": "C",
    "組織名": "A",
    "指示詞": "d",
    "副詞": "a",
    "助詞": "p",
    "接続詞": "c",
    "連体詞": "m",
    "感動詞": "!",
    "接頭辞": "p",
    "接尾辞": "s",
    "未定義語": "?",
}


def draw_tree(
    leaves: Sequence[Union["Phrase", "BasePhrase"]],
    fh: TextIO = sys.stdout,
    show_pos: bool = True,
) -> None:
    """構文木を指定された fh に出力する．"""
    print(sprint_tree(leaves, show_pos=show_pos), file=fh, end="")


def sprint_tree(leaves: Sequence[Union["Phrase", "BasePhrase"]], show_pos: bool = True) -> str:
    """構文木を文字列で返す．"""
    limit = len(leaves)
    item = [[""] * limit for _ in leaves]
    active_column = [0] * limit
    limit -= 1

    for i in range(limit):
        parent_index = leaves[i].parent_index
        dep_type = leaves[i].dep_type
        assert parent_index is not None, "parent_index has not been set"
        para_row = leaves[i].dep_type == DepType.PARALLEL
        for j in range(i + 1, limit + 1):
            if j < parent_index:
                if active_column[j] == 2:
                    item[i][j] = "╋" if para_row else "╂"
                elif active_column[j] == 1:
                    item[i][j] = "┿" if para_row else "┼"
                else:
                    item[i][j] = "━" if para_row else "─"
            elif j == parent_index:
                if dep_type == DepType.PARALLEL:
                    item[i][j] = "Ｐ"
                elif dep_type == DepType.IMPERFECT_PARALLEL:
                    item[i][j] = "Ｉ"
                elif dep_type == DepType.APPOSITION:
                    item[i][j] = "Ａ"
                else:
                    if active_column[j] == 2:
                        item[i][j] = "┨"
                    elif active_column[j] == 1:
                        item[i][j] = "┤"
                    else:
                        item[i][j] = "┐"
                if active_column[j] == 2:
                    # すでにＰからの太線があればそのまま
                    pass
                elif para_row:
                    active_column[j] = 2
                else:
                    active_column[j] = 1
            else:
                if active_column[j] == 2:
                    item[i][j] = "┃"
                elif active_column[j] == 1:
                    item[i][j] = "│"
                else:
                    item[i][j] = "　"

    lines = [_leaf_string(leaf, show_pos) for leaf in leaves]
    for i in range(limit):
        for j in range(i + 1, limit + 1):
            lines[i] += item[i][j]

    max_length = max(_str_real_length(line) for line in lines)
    buf = ""
    for i in range(limit + 1):
        diff = max_length - _str_real_length(lines[i])
        buf += " " * diff
        buf += lines[i] + "\n"

    return buf


def _leaf_string(leaf: Union["Phrase", "BasePhrase"], show_pos: bool) -> str:
    ret = ""
    for mrph in leaf.morphemes:
        ret += mrph.text
        if show_pos is True:
            if re.search("^(?:固有名詞|人名|地名)$", mrph.subpos):
                ret += POS_MARK[mrph.subpos]
            else:
                ret += POS_MARK[mrph.pos]
    return ret


def _str_real_length(string: str) -> int:
    length = 0
    for char in string:
        if re.search(r"^[a-zA-Z*!?]$", char):
            # 品詞情報は長さ1
            length += 1
        else:
            length += 2
    return length
