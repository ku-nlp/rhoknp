"""Example code for applying KWJA to the given sentence.

Usage:
    $ python examples/apply_knp.py "今日はいい天気ですね。"
"""
import sys

from rhoknp import KWJA

# Create a KWJA instance.
kwja = KWJA()

# Apply KNP to a sentence.
sent = kwja.apply_to_sentence(sys.argv[1])

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
