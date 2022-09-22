"""Example code for loading Juman++ from a file.

Usage:
    $ python examples/load_jumanpp.py example.jumanpp
"""
import sys

from rhoknp import Sentence
from rhoknp.utils.reader import chunk_by_sentence

with open(sys.argv[1]) as f:
    for jumanpp in chunk_by_sentence(f):
        sent = Sentence.from_jumanpp(jumanpp)
        print(f"Successfully loaded a sentence: {sent.text}")
