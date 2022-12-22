import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class MemoTag:
    """関係タグ付きコーパスにおける <memo> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern] = re.compile(r'<memo text="(?P<text>.*?)"/>')
    text: str = ""  #: メモの内容．

    @classmethod
    def from_fstring(cls, fstring: str) -> "MemoTag":
        """KNP における素性文字列からオブジェクトを作成．"""
        match = cls.PAT.search(fstring)
        memo_tag = MemoTag(text=match["text"] if match is not None else "")
        return memo_tag

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f'<memo text="{self.text}"/>'

    def __str__(self) -> str:
        return self.to_fstring()

    def __bool__(self) -> bool:
        return bool(self.text)
