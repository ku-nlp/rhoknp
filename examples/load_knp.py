"""Example code for loading KNP from a file.

Usage:
    $ python examples/load_knp.py example.jumanpp
"""
import sys

from rhoknp import Sentence
from rhoknp.utils.reader import chunk_by_sentence

with open(sys.argv[1]) as f:
    for knp in chunk_by_sentence(f):
        sent = Sentence.from_knp(knp)
        print(f"Successfully loaded a sentence: {sent.text}")
