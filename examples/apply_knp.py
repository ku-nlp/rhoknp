"""Example code for applying KNP to the given sentence.

Usage:
    $ python examples/apply_knp.py "今日はいい天気ですね。"
"""
import sys

from rhoknp import KNP

# Create a KNP instance.
knp = KNP()

# Apply KNP to a sentence.
sent = knp.apply_to_sentence(sys.argv[1])

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
