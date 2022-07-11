import copy
import logging
import re
from collections import defaultdict
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional, Union

from rhoknp.rel.argument import Argument, ArgumentType, BaseArgument, SpecialArgument
from rhoknp.rel.exophora import ExophoraReferent
from rhoknp.rel.predicate import Predicate
from rhoknp.units.utils import RelMode

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase

logger = logging.getLogger(__name__)


class CaseInfoFormat(Enum):
    CASE = auto()  # 格解析フォーマット
    PAS = auto()  # 述語項構造フォーマット


class Pas:
    ARGUMENT_PAT = re.compile(r"([^/;]+/[CNODEU-]/[^/]+/(-?\d*)/(-?\d*)/[^/;]+)")  # ガ/N/彼/0/0/5

    def __init__(self, predicate: Predicate):
        self._predicate = predicate
        predicate.pas = self
        self._arguments: dict[str, list[BaseArgument]] = defaultdict(list)
        self.modes: dict[str, RelMode] = {}

    @property
    def predicate(self) -> Predicate:
        return self._predicate

    @property
    def cases(self) -> list[str]:
        return [case for case, args in self._arguments.items() if args]

    @property
    def sid(self) -> str:
        return self._predicate.sid

    @classmethod
    def from_pas_string(cls, base_phrase: "BasePhrase", fstring: str, format_: CaseInfoFormat) -> "Pas":
        # language=RegExp
        cfid_pat = r"(.*?):([^:/]+?)"  # 食べる/たべる:動1
        match = re.match(
            r"{cfid}(:(?P<args>{args}(;{args})*))?$".format(cfid=cfid_pat, args=cls.ARGUMENT_PAT.pattern),
            fstring,
        )

        if match is None:
            logger.warning(f"invalid tag format: '{fstring}' is ignored")
            return cls(Predicate(base_phrase))

        cfid = match.group(1) + ":" + match.group(2)
        predicate = Predicate(unit=base_phrase, cfid=cfid)

        if match.group(3) is None:  # <述語項構造:束の間/つかのま:判0> など
            return cls(predicate)

        pas = cls(predicate)
        for match_arg in cls.ARGUMENT_PAT.finditer(match.group("args")):
            case, case_flag, surf, *fields = match_arg.group(0).split("/")
            if case_flag in ("U", "-"):
                continue
            arg_type = ArgumentType(case_flag)
            arg: BaseArgument
            if format_ == CaseInfoFormat.CASE:
                tid, sdist, sid = int(fields[0]), int(fields[1]), fields[2]
                assert arg_type != ArgumentType.EXOPHORA
                if sdist == 0:
                    sentence = base_phrase.sentence
                else:
                    if (sentence_index := base_phrase.sentence.index - sdist) < 0:
                        logger.warning(f"sentence index out of range: {sentence_index} in {base_phrase.sentence.sid}")
                        continue
                    sentence = base_phrase.document.sentences[sentence_index]
                assert sentence.sid == sid
                arg_base_phrase = sentence.base_phrases[tid]
                assert surf in arg_base_phrase.text
                pas.add_argument(case, arg_base_phrase, arg_type=arg_type)
            else:
                assert format_ == CaseInfoFormat.PAS
                sdist, tid, eid = int(fields[0]), int(fields[1]), int(fields[2])
                if arg_type == ArgumentType.EXOPHORA:
                    pas.add_special_argument(case, surf, eid)
                else:
                    if sdist == 0:
                        sentence = base_phrase.sentence
                    else:
                        if (sentence_index := base_phrase.sentence.index - sdist) < 0:
                            logger.warning(
                                f"sentence index out of range: {sentence_index} in {base_phrase.sentence.sid}"
                            )
                            continue
                        sentence = base_phrase.document.sentences[sentence_index]
                    arg_base_phrase = sentence.base_phrases[tid]
                    assert surf in arg_base_phrase.text
                    pas.add_argument(case, arg_base_phrase)
        return pas

    def get_arguments(
        self,
        case: str,
        relax: bool = True,
        include_nonidentical: bool = False,
        include_optional: bool = False,
    ) -> list[BaseArgument]:
        """与えられた格の全ての項を返す．

        Args:
            case: 格．
            relax: True なら 共参照関係で結ばれた項も含めて出力する．
            include_nonidentical: True なら nonidentical な項も含めて出力する．
            include_optional: True なら修飾的表現（「すぐに」など）も含めて出力する．

        References:
            格・省略・共参照タグ付けの基準 3.2.1 修飾的表現

        Returns: 項のリスト．
        """
        args = self._arguments[case]
        if include_nonidentical is True:
            args += self._arguments[case + "≒"]
        if include_optional is False:
            args = [arg for arg in args if arg.optional is False]
        pas = copy.copy(self)
        pas._arguments[case] = copy.copy(args)

        sentence = self.predicate.base_phrase.sentence
        if relax is True and sentence.parent_unit is not None:
            entity_manager = sentence.document.entity_manager
            for arg in args:
                if isinstance(arg, SpecialArgument):
                    entities = {entity_manager[arg.eid]}
                else:
                    assert isinstance(arg, Argument)
                    entities = arg.base_phrase.entities_all if include_nonidentical else arg.base_phrase.entities
                for entity in entities:
                    if entity.exophora_referent is not None:
                        pas.add_special_argument(case, entity.exophora_referent, entity.eid)
                    for mention in entity.mentions:
                        if isinstance(arg, Argument) and mention == arg.base_phrase:
                            continue
                        pas.add_argument(case, mention)
        return pas._arguments[case]

    def get_all_arguments(
        self,
        relax: bool = True,
        include_nonidentical: bool = False,
        include_optional: bool = False,
    ) -> dict[str, list[BaseArgument]]:
        """この述語項構造が持つ全ての項を格を key とする辞書形式で返す．

        Args:
            relax: True なら 共参照関係で結ばれた項も含めて出力する．
            include_nonidentical: True なら nonidentical な項も含めて出力する．
            include_optional: True なら修飾的表現（「すぐに」など）も含めて出力する．

        Returns: 格を key とする項の辞書．
        """
        all_arguments: dict[str, list[BaseArgument]] = {}
        for case in self.cases:
            all_arguments[case] = self.get_arguments(
                case,
                relax=relax,
                include_nonidentical=include_nonidentical,
                include_optional=include_optional,
            )
        return all_arguments

    def add_argument(
        self,
        case: str,
        base_phrase: "BasePhrase",
        mode: Optional[RelMode] = None,
        arg_type: Optional[ArgumentType] = None,
    ) -> None:
        argument = Argument(
            base_phrase,
            arg_type or self._get_arg_type(self.predicate, base_phrase, case),
        )
        argument.pas = self
        if mode is not None:
            self.modes[case] = mode
        if argument not in self._arguments[case]:
            self._arguments[case].append(argument)

    def add_special_argument(
        self, case: str, exophora_referent: Union[ExophoraReferent, str], eid: int, mode: Optional[RelMode] = None
    ) -> None:
        if isinstance(exophora_referent, str):
            exophora_referent = ExophoraReferent(exophora_referent)
        special_argument = SpecialArgument(exophora_referent, eid)
        special_argument.pas = self
        if mode is not None:
            self.modes[case] = mode
        if special_argument not in self._arguments[case]:
            self._arguments[case].append(special_argument)

    def set_arguments_optional(self, case: str) -> None:
        if not self._arguments[case]:
            logger.info(f"no preceding argument found in {self.sid}. 'なし' is ignored")
            return
        for arg in self._arguments[case]:
            arg.optional = True
            logger.info(f"marked {arg} as optional in {self.sid}")

    @staticmethod
    def _get_arg_type(predicate: Predicate, arg_base_phrase: "BasePhrase", case: str) -> ArgumentType:
        if arg_base_phrase in predicate.base_phrase.children:
            dep_case = arg_base_phrase.features.get("係", "")
            assert isinstance(dep_case, str)
            dep_case = dep_case.rstrip("格")
            if (case == dep_case) or (case == "判ガ" and dep_case == "ガ") or (case == "ノ？" and dep_case == "ノ"):
                return ArgumentType.CASE_EXPLICIT
            else:
                return ArgumentType.CASE_HIDDEN
        elif predicate.base_phrase.parent and predicate.base_phrase.parent == arg_base_phrase:
            return ArgumentType.CASE_HIDDEN
        else:
            return ArgumentType.OMISSION

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(predicate={repr(self.predicate)}, arguments={repr(dict(self._arguments))})"
