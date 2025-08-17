"""Example code for using the result of coreference resolution.

Usage:
    $ python examples/use_coreference_resolution.py "ソビエト連邦はソ連ともよばれる。同国の首都はモスクワである。"
"""

import sys

from rhoknp import KWJA, BasePhrase

# Create a KWJA instance.
kwja = KWJA(options=["--model-size", "tiny"])  # `tiny`, `base`, or `large`

# Apply KWJA to a document.
doc = kwja.apply_to_document(sys.argv[1], timeout=120)

# Get information.
for base_phrase in doc.base_phrases:
    coreferents: list[BasePhrase] = base_phrase.get_coreferents()
    if len(coreferents) > 0:
        print(f"Mention {base_phrase}")
        for coreferring_mention in coreferents:
            print(f"  = {coreferring_mention}")
        print("---")
