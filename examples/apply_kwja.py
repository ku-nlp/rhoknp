"""Example code for applying KWJA to the given sentence.

Usage:
    $ python examples/apply_kwja.py "今日はいい天気ですね。"
"""
import sys

from rhoknp import KWJA

# Create a KWJA instance.
kwja = KWJA()

# Apply KWJA to a document.
doc = kwja.apply_to_document(sys.argv[1])

# Get information.
for mrph in doc.morphemes:
    print(f"Text: {mrph.text}")
    print(f"Reading: {mrph.reading}")
    print(f"Lemma: {mrph.lemma}")
    print(f"POS: {mrph.pos}")
    print(f"Sub POS: {mrph.subpos}")
    print(f"Conjugation (type): {mrph.conjtype}")
    print(f"Conjugation (form): {mrph.conjform}")
    print("---")
