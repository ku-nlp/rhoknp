"""Example code for applying Juman++ to the given sentence.

Usage:
    $ python examples/apply_jumanpp.py "今日はいい天気ですね。"
"""

import sys

from rhoknp import Jumanpp

# Create a Jumanpp instance.
jumanpp = Jumanpp()

# Apply Jumanpp to a sentence.
sent = jumanpp.apply_to_sentence(sys.argv[1])

# Get information.
for mrph in sent.morphemes:
    print(f"Text: {mrph.text}")
    print(f"Reading: {mrph.reading}")
    print(f"Lemma: {mrph.lemma}")
    print(f"POS: {mrph.pos}")
    print(f"Sub POS: {mrph.subpos}")
    print(f"Conjugation (type): {mrph.conjtype}")
    print(f"Conjugation (form): {mrph.conjform}")
    print("---")
