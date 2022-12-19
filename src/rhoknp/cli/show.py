import sys
from typing import List, Sequence, TextIO, Union

from rich.console import Console
from rich.table import Table
from rich.text import Text

from rhoknp.props.dependency import DepType
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
    leaves: Union[Sequence[Phrase], Sequence[BasePhrase]],
    fh: TextIO = sys.stdout,
    show_pos: bool = False,
    show_rel: bool = False,
) -> None:
    """構文木を指定された fh に出力．

    Args:
        leaves: 構文木の葉となる文節列または基本句列．
        fh: 出力先．
        show_pos: True なら同時に品詞を表示する．
        show_rel: True なら同時に <rel> タグを表示する．
    """
    console = Console(file=fh)
    table = Table.grid(padding=(0, 2))
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
                if dep_type in (DepType.PARALLEL, DepType.IMPERFECT_PARALLEL, DepType.APPOSITION):
                    item[i][j] = str(dep_type.value)
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
                    item[i][j] = " "

    lines: List[str] = []
    for i in range(len(leaves)):
        line = _leaf_string(leaves[i], show_pos)
        for j in range(i + 1, len(leaves)):
            line += _extend_horizontal(item[i][j]) + item[i][j]
        lines.append(line)

    max_length = max(_str_real_length(line) for line in lines)
    for line, leaf in zip(lines, leaves):
        diff = max_length - _str_real_length(line)
        tree_string = " " * diff + line
        rel_string = _rel_string(leaf) if isinstance(leaf, BasePhrase) and show_rel is True else ""
        table.add_row(Text(tree_string), Text(rel_string))
    console.print(table)


def _extend_horizontal(token: str) -> str:
    if token in ("╂", "┼", "┤", "┨", "┐", "─", "I", "A"):
        return "─"
    elif token in ("╋", "┿", "━", "P"):
        return "━"
    else:
        return " "


def _leaf_string(leaf: Union[Phrase, BasePhrase], show_pos: bool) -> str:
    ret = ""
    for morpheme in leaf.morphemes:
        ret += morpheme.text
        if show_pos is True:
            if morpheme.subpos in ("固有名詞", "人名", "地名"):
                ret += POS_MARK[morpheme.subpos]
            else:
                ret += POS_MARK[morpheme.pos]
    return ret


def _str_real_length(string: str) -> int:
    return Text(string).cell_len


def _rel_string(base_phrase: BasePhrase) -> str:
    return " ".join(f"{tag.type}:{tag.target}" for tag in base_phrase.rel_tags)
