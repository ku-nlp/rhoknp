"""Example code for using the result of named entity recognition.

Usage:
    $ python examples/use_named_entity_recognition.py "太郎は花子が読んでいる本を次郎に渡した。"
"""

import sys

from rhoknp import KNP

# Create a KNP instance.
knp = KNP()

# Apply KNP to a sentence.
sent = knp.apply_to_sentence(sys.argv[1])

# Get information.
if sent.named_entities:
    print(f"Found {len(sent.named_entities)} named entities:")
    for i, named_entity in enumerate(sent.named_entities, start=1):
        print(f'  {i}. "{named_entity.text}" ({named_entity.category.value})')
else:
    print("No named entity found.")
