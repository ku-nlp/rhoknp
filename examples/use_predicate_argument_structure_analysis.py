"""Example code for using the result of predicate-argument structure analysis.

Usage:
    $ python examples/use_predicate_argument_structure_analysis.py "太郎は花子が読んでいる本を次郎に渡した。"
"""

import sys

from rhoknp import KWJA
from rhoknp.cohesion import Argument

# Create a KWJA instance.
kwja = KWJA(options=["--model-size", "tiny"])  # `tiny`, `base`, or `large`

# Apply KWJA to a document.
doc = kwja.apply_to_document(sys.argv[1], timeout=120)

# Get information.
for base_phrase in doc.base_phrases:
    pas = base_phrase.pas
    if pas.is_empty() is True:
        continue
    all_arguments: dict[str, list[Argument]] = pas.get_all_arguments()
    print(f"Predicate: {pas.predicate}")
    for case, arguments in all_arguments.items():
        print(f"  {case}格: ", end="")
        print(", ".join(str(argument) for argument in arguments))
    print("---")
