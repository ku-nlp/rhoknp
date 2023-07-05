import logging
import re
from typing import List, Optional, Tuple

from rhoknp.units.morpheme import Morpheme

logger = logging.getLogger(__name__)


def is_comment_line(line: str) -> bool:
    """行がコメント行かどうかを判定する．

    Args:
        line: 行．

    Returns:
        bool: コメント行ならTrue．
    """
    return line.startswith("#") and not Morpheme.is_morpheme_line(line)


def extract_did_and_sid(comment_line: str, patterns: List[re.Pattern]) -> Tuple[Optional[str], Optional[str], str]:
    """コメント行から文書IDおよび文IDを抽出する．

    Args:
        comment_line: コメント行．
        patterns: 文書IDを抽出する正規表現のリスト．最初にマッチしたものが使用される．

    Returns:
        Optional[str]: 文書ID（見つからなければNone）．
        Optional[str]: 文ID（見つからなければNone）．
        str: 残りのコメント行．
    """
    match_sid = re.match(r"# S-ID: ?(\S*)( .+)?$", comment_line)
    if match_sid is not None:
        sid_string = match_sid[1]
        for pattern in patterns:
            match = pattern.match(sid_string)
            if match is not None:
                return match["did"], match["sid"], match_sid[2].lstrip() if match_sid[2] else ""
        logger.warning(f"Invalid S-ID: {sid_string}")
    return None, None, comment_line.lstrip("#").lstrip()
