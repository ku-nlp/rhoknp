"""Example code for using the result of dependency parsing.

Usage:
    $ python examples/use_dependency_parsing.py "今日はいい天気ですね。"
"""

import sys

from rhoknp import KNP

# Create a KNP instance.
knp = KNP()

# Apply KNP to a sentence.
sent = knp.apply_to_sentence(sys.argv[1])

# Get information.
for phrase in sent.phrases:
    parent = phrase.parent
    if parent:
        print(f"{phrase.text} -> {parent.text}")
    else:
        print(f"{phrase.text} -> ROOT")
