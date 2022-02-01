import re
import sys
from collections import defaultdict
from enum import Enum, auto
from typing import Optional

from rhoknp.pas.argument import Argument, ArgumentType, BaseArgument, SpecialArgument
from rhoknp.pas.predicate import Predicate
from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.utils import RelMode


class CaseInfoFormat(Enum):
    CASE = auto()  # 格解析フォーマット
    PAS = auto()  # 述語項構造フォーマット


class Pas:
    ARGUMENT_PAT = re.compile(
        r"([^/;]+/[CNODEU-]/[^/]+/(-?\d*)/(-?\d*)/[^/;]+)"
    )  # ガ/N/彼/0/0/5

    def __init__(self, predicate: Predicate):
        self._predicate = predicate
        predicate.pas = self
        self._arguments: dict[str, list[BaseArgument]] = defaultdict(list)
        self.modes: dict[str, RelMode] = {}

    @property
    def predicate(self) -> Predicate:
        return self._predicate

    @property
    def arguments(self) -> dict[str, list[BaseArgument]]:
        return self._arguments

    @classmethod
    def _from_pas_string(
        cls, base_phrase: BasePhrase, fstring: str, format_: CaseInfoFormat
    ) -> "Pas":
        # language=RegExp
        cfid_pat = r"(.*?):([^:/]+?)"  # 食べる/たべる:動1
        match = re.match(
            r"{cfid}(:(?P<args>{args}(;{args})*))?$".format(
                cfid=cfid_pat, args=cls.ARGUMENT_PAT.pattern
            ),
            fstring,
        )

        if match is None:
            print(f"invalid tag format: '{fstring}' is ignored", file=sys.stderr)
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
                assert arg_type != ArgumentType.EXOPHOR
                assert (
                    base_phrase.document.sentences[
                        base_phrase.sentence.index - sdist
                    ].sid
                    == sid
                )
                arg_base_phrase = base_phrase.document.sentences[
                    base_phrase.sentence.index - sdist
                ].base_phrases[tid]
                assert surf in arg_base_phrase.text
                pas.add_argument(case, arg_base_phrase, arg_type=arg_type)
            else:
                assert format_ == CaseInfoFormat.PAS
                sdist, tid, eid = int(fields[0]), int(fields[1]), int(fields[2])
                if arg_type == ArgumentType.EXOPHOR:
                    pas.add_special_argument(case, surf, eid)
                else:
                    arg_base_phrase = base_phrase.document.sentences[
                        base_phrase.sentence.index - sdist
                    ].base_phrases[tid]
                    assert surf in arg_base_phrase.text
                    pas.add_argument(case, arg_base_phrase)
        return pas

    @classmethod
    def from_base_phrase(cls, base_phrase: BasePhrase) -> "Pas":
        if "述語項構造" in base_phrase.features:
            pas_string = base_phrase.features["述語項構造"]
            assert isinstance(pas_string, str)
            pas = cls._from_pas_string(
                base_phrase, pas_string, format_=CaseInfoFormat.PAS
            )
        elif "格解析結果" in base_phrase.features:
            pas_string = base_phrase.features["格解析結果"]
            assert isinstance(pas_string, str)
            pas = cls._from_pas_string(
                base_phrase, pas_string, format_=CaseInfoFormat.CASE
            )
        else:
            pas = cls(Predicate(base_phrase))
        base_phrase.pas = pas
        return pas

    def add_argument(
        self,
        case: str,
        base_phrase: BasePhrase,
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
        if argument not in self.arguments[case]:
            self.arguments[case].append(argument)

    def add_special_argument(
        self, case: str, exophor: str, eid: int, mode: Optional[RelMode] = None
    ) -> None:
        special_argument = SpecialArgument(exophor, eid)
        special_argument.pas = self
        if mode is not None:
            self.modes[case] = mode
        if special_argument not in self.arguments[case]:
            self.arguments[case].append(special_argument)

    @staticmethod
    def _get_arg_type(
        predicate: Predicate, arg_base_phrase: BasePhrase, case: str
    ) -> ArgumentType:
        if arg_base_phrase in predicate.phrase.children:
            dep_case = arg_base_phrase.features.get("係", "")
            assert isinstance(dep_case, str)
            dep_case = dep_case.rstrip("格")
            if (
                (case == dep_case)
                or (case == "判ガ" and dep_case == "ガ")
                or (case == "ノ？" and dep_case == "ノ")
            ):
                return ArgumentType.CASE_EXPLICIT
            else:
                return ArgumentType.CASE_HIDDEN
        elif predicate.phrase.parent and predicate.phrase.parent == arg_base_phrase:
            return ArgumentType.CASE_HIDDEN
        else:
            return ArgumentType.OMISSION

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(predicate={repr(self.predicate)}, arguments={repr(dict(self.arguments))})"
