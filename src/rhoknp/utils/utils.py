def is_comment_line(line: str) -> bool:
    """コメント行なら True を返す．"""
    return line.startswith("# ") and not line.startswith("# # # 未定義語 15 その他 1 * 0 * 0")
