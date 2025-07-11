import copy
import logging
import re
from collections import defaultdict
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional

from rhoknp.cohesion import EntityManager
from rhoknp.cohesion.argument import HIRA2KATA, Argument, ArgumentType, EndophoraArgument, ExophoraArgument
from rhoknp.cohesion.exophora import ExophoraReferent
from rhoknp.cohesion.predicate import Predicate
from rhoknp.cohesion.rel import CASE_TYPES, RelMode

NUM_HAN_TO_ZEN = str.maketrans("0123456789", "０１２３４５６７８９")

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase

logger = logging.getLogger(__name__)


class CaseInfoFormat(Enum):
    """各解析のフォーマットを表す列挙体．"""

    CASE = auto()  #: 格解析フォーマット．
    PAS = auto()  #: 述語項構造フォーマット．


class Pas:
    """述語項構造クラス．

    Args:
        predicate: 述語．
    """

    # matches for "ガ/N/彼/0/0/5"
    ARGUMENT_PAT = re.compile(rf"([^/;]+/[{''.join(e.value for e in ArgumentType)}-]/[^/]+/(-?\d*)/(-?\d*)/[^/;]+)")

    def __init__(self, predicate: Predicate) -> None:
        self._predicate = predicate
        predicate.pas = self
        self._arguments: dict[str, list[Argument]] = defaultdict(list)
        self.modes: dict[str, RelMode] = {}

    @property
    def predicate(self) -> Predicate:
        """述語．"""
        return self._predicate

    @property
    def cases(self) -> list[str]:
        """属する全ての項の持つ格を集めたリスト．"""
        return [case for case, args in self._arguments.items() if args]

    @property
    def sid(self) -> str:
        """文 ID．"""
        return self._predicate.sid

    def is_empty(self) -> bool:
        """述語が項を持たなければ True．"""
        for args in self._arguments.values():
            if len(args) > 0:
                return False
        return True

    def parse_pas_string(self, base_phrase: "BasePhrase", pas_string: str, format_: CaseInfoFormat) -> None:
        """PAS 文字列から述語項構造を生成する．

        Args:
            base_phrase: 述語となる基本句．
            pas_string: 述語項構造を表す素性文字列（e.g., "食べる/たべる:動2:ガ/C/太郎/0/0/1;ヲ/C/パン/1/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-"）
            format_: fstring における述語項構造のフォーマット．
        """
        # language=RegExp
        cfid_pat = r"(.*?):([^:/]+?)"  # 食べる/たべる:動1
        match = re.match(
            r"{cfid}(:(?P<args>{args}(;{args})*))?$".format(  # noqa: UP032
                cfid=cfid_pat, args=self.ARGUMENT_PAT.pattern
            ),
            pas_string,
        )

        if match is None:
            logger.warning(f"ignored malformed pas_string: '{pas_string}'")
            return

        self.predicate.cfid = f"{match[1]}:{match[2]}"

        if match[3] is None:  # <述語項構造:束の間/つかのま:判0> など
            return

        for match_arg in self.ARGUMENT_PAT.finditer(match["args"]):
            case, case_flag, surf, *fields = match_arg[0].split("/")
            if case_flag in ("U", "-"):
                continue
            arg_type = ArgumentType(case_flag)
            if format_ == CaseInfoFormat.CASE:
                tid, sdist, sid = int(fields[0]), int(fields[1]), fields[2]
                assert arg_type != ArgumentType.EXOPHORA
                if sdist == 0:
                    sentence = base_phrase.sentence
                else:
                    sentence_index = base_phrase.sentence.index - sdist
                    if sentence_index < 0:
                        logger.warning(f"sentence index out of range: {sentence_index} in {base_phrase.sentence.sid}")
                        continue
                    sentence = base_phrase.document.sentences[sentence_index]
                assert sentence.sid == sid, f"sentence id mismatch: '{sentence.sid}' vs '{sid}'"
                arg_base_phrase = sentence.base_phrases[tid]
                if surf not in arg_base_phrase.text:
                    logger.warning(f"surface mismatch ({sid}): '{surf}' vs '{arg_base_phrase.text}'")
                self.add_argument(EndophoraArgument(case, arg_base_phrase, self.predicate, arg_type=arg_type))
            elif format_ == CaseInfoFormat.PAS:
                sdist, tid, eid = int(fields[0]), int(fields[1]), int(fields[2])
                if arg_type == ArgumentType.EXOPHORA:
                    self.add_argument(ExophoraArgument(case, ExophoraReferent(surf), eid))
                else:
                    if sdist == 0:
                        sentence = base_phrase.sentence
                    else:
                        sentence_index = base_phrase.sentence.index - sdist
                        if sentence_index < 0:
                            logger.warning(
                                f"sentence index out of range: {sentence_index} in {base_phrase.sentence.sid}"
                            )
                            continue
                        sentence = base_phrase.document.sentences[sentence_index]
                    if not 0 <= tid < len(sentence.base_phrases):
                        logger.warning(f"{sentence.sid}: tag id out of range: {tid}")
                        continue
                    arg_base_phrase = sentence.base_phrases[tid]
                    if surf not in arg_base_phrase.text:
                        logger.warning(f"surface mismatch ({sentence.sid}): '{surf}' vs '{arg_base_phrase.text}'")
                    self.add_argument(EndophoraArgument(case, arg_base_phrase, self.predicate))
            else:
                raise AssertionError(f"invalid format: {format_}")

    def get_arguments(
        self,
        case: str,
        relax: bool = True,
        include_nonidentical: bool = False,
        include_optional: bool = False,
    ) -> list[Argument]:
        """与えられた格の全ての項を返す．

        Args:
            case: 格．
            relax: True なら 共参照関係で結ばれた項も含めて出力する．
            include_nonidentical: True なら nonidentical な項も含めて出力する．
            include_optional: True なら修飾的表現（「すぐに」など）も含めて出力する．

        References:
            格・省略・共参照タグ付けの基準 3.2.1 修飾的表現
        """
        case = normalize_case(case)
        args = self._arguments[case]
        if include_nonidentical is True:
            args += self._arguments[case + "≒"]
        if include_optional is False:
            args = [arg for arg in args if arg.optional is False]
        pas = copy.copy(self)
        pas._arguments = copy.copy(self._arguments)
        pas._arguments[case] = copy.copy(args)

        sentence = self.predicate.base_phrase.sentence
        if relax is True and sentence.parent_unit is not None:
            for arg in args:
                if isinstance(arg, ExophoraArgument):
                    entities = {EntityManager.get_or_create_entity(eid=arg.eid)}
                elif isinstance(arg, EndophoraArgument):
                    entities = arg.base_phrase.entities_all if include_nonidentical else arg.base_phrase.entities
                else:
                    raise AssertionError  # noqa: TRY004, unreachable
                for entity in entities:
                    if entity.exophora_referent is not None:
                        pas.add_argument(ExophoraArgument(case, entity.exophora_referent, entity.eid))
                    for mention in entity.mentions:
                        if isinstance(arg, EndophoraArgument) and mention == arg.base_phrase:
                            continue
                        pas.add_argument(EndophoraArgument(case, mention, pas.predicate))
        return pas._arguments[case]

    def get_all_arguments(
        self,
        relax: bool = True,
        include_nonidentical: bool = False,
        include_optional: bool = False,
    ) -> dict[str, list[Argument]]:
        """この述語項構造が持つ全ての項を格を key とする辞書形式で返す．

        Args:
            relax: True なら 共参照関係で結ばれた項も含めて出力する．
            include_nonidentical: True なら nonidentical な項も含めて出力する．
            include_optional: True なら修飾的表現（「すぐに」など）も含めて出力する．
        """
        all_arguments: dict[str, list[Argument]] = {}
        for case in self.cases:
            all_arguments[case] = self.get_arguments(
                case,
                relax=relax,
                include_nonidentical=include_nonidentical,
                include_optional=include_optional,
            )
        return all_arguments

    def add_argument(self, argument: Argument, mode: Optional[RelMode] = None) -> None:
        """述語項構造に項を追加．

        Args:
            argument: 追加する項．
            mode: 関係のモード．
        """
        case = argument.case
        argument.pas = self
        if mode is not None:
            self.modes[case] = mode
        if argument not in self._arguments[case]:
            self._arguments[case].append(argument)

    def set_arguments_optional(self, case: str) -> None:
        """与えられた格に属する項をすべて修飾的表現として登録．

        Args:
            case: 対象の格．
        """
        case = normalize_case(case)
        if not self._arguments[case]:
            logger.info(f"no preceding argument found in {self.sid}. 'なし' is ignored")
            return
        for arg in self._arguments[case]:
            arg.optional = True
            logger.info(f"marked {arg} as optional in {self.sid}")

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {self.predicate.text!r}>"


def normalize_case(case: str) -> str:
    """格を表す文字列を正規化．

    Args:
        case: 格．

    Returns:
        正規化された格．
    """
    case = case.translate(NUM_HAN_TO_ZEN)
    if case.translate(HIRA2KATA) in CASE_TYPES:
        return case.translate(HIRA2KATA)
    return case
