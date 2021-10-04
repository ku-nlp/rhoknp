import re
import sys
from collections import defaultdict
from enum import Enum, auto
from typing import Dict, List

from rhoknp.units import Phrase

from .argument import Argument, ArgumentType, BaseArgument, SpecialArgument
from .predicate import Predicate


class CaseInfoFormat(Enum):
    CASE = auto()  # 格解析フォーマット
    PAS = auto()  # 述語項構造フォーマット


class Pas:
    ARGUMENT_PATTERN = re.compile(r"([^/;]+/[CNODEU-]/[^/]+/(-?\d*)/(-?\d*)/[^/;]+)")  # ガ/N/彼/0/0/5

    def __init__(self, predicate: Predicate, arguments: Dict[str, List[BaseArgument]]):
        self.predicate = predicate
        self.arguments = arguments

    @classmethod
    def from_pas_string(cls, phrase: Phrase, fstring: str, format_: CaseInfoFormat) -> "Pas":
        arguments: Dict[str, List[BaseArgument]] = defaultdict(list)

        # language=RegExp
        cfid_pat = r"(.*?):([^:/]+?)"  # 食べる/たべる:動1
        match = re.match(
            r"{cfid}(:(?P<args>{args}(;{args})*))?$".format(cfid=cfid_pat, args=cls.ARGUMENT_PATTERN.pattern), fstring
        )

        if match is None:
            print(f"invalid tag format: '{fstring}' is ignored", file=sys.stderr)
            return cls(Predicate(phrase), {})

        cfid = match.group(1) + ":" + match.group(2)
        predicate = Predicate(unit=phrase, cfid=cfid)

        if match.group(3) is None:  # <述語項構造:束の間/つかのま:判0> など
            return cls(predicate, {})

        for match_arg in cls.ARGUMENT_PATTERN.finditer(match.group("args")):
            case, caseflag, midasi, *fields = match_arg.group(0).split("/")
            if caseflag in ("U", "-"):
                continue
            arg_type = ArgumentType.value_of(caseflag)
            arg: BaseArgument
            if format_ == CaseInfoFormat.CASE:
                tid, sdist, sid = int(fields[0]), int(fields[1]), fields[2]
                assert arg_type != ArgumentType.exophor
                assert phrase.document.sentences[phrase.sentence.index - sdist].sid == sid
                arg_phrase = phrase.document.sentences[phrase.sentence.index - sdist].phrases[tid]
                assert midasi in arg_phrase.text
                arg = Argument(phrase=arg_phrase, arg_type=arg_type)
            else:
                assert format_ == CaseInfoFormat.PAS
                sdist, tid, eid = int(fields[0]), int(fields[1]), int(fields[2])
                if arg_type == ArgumentType.exophor:
                    arg = SpecialArgument(exophor=midasi, eid=eid)
                else:
                    arg_phrase = phrase.document.sentences[phrase.sentence.index - sdist].phrases[tid]
                    assert midasi in arg_phrase.text
                    arg = Argument(phrase=arg_phrase, arg_type=arg_type)
            arguments[case].append(arg)

        return cls(predicate, arguments)

    @classmethod
    def from_phrase(cls, phrase: Phrase) -> "Pas":
        if "述語項構造" in phrase.features:
            pas_string = phrase.features["述語項構造"]
            return cls.from_pas_string(phrase, pas_string, format_=CaseInfoFormat.PAS)
        elif "格解析結果" in phrase.features:
            pas_string = phrase.features["格解析結果"]
            return cls.from_pas_string(phrase, pas_string, format_=CaseInfoFormat.CASE)
        else:
            return cls(Predicate(phrase), {})
