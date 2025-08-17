"""Example code for using the result of morphological analysis.

Usage:
    $ python examples/use_morphological_analysis.py "今日はいい天気ですね。"
"""

import sys

from rhoknp import Jumanpp

# Create a Jumanpp instance.
jumanpp = Jumanpp()  # or `kwja = KWJA()`

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
