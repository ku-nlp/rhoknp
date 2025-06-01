"""Example code for using the result of discourse relation analysis.

Usage:
    $ python examples/use_discourse_relation_analysis.py "風が吹いたら桶屋が儲かる。"
"""

import sys

from rhoknp import KNP

# Create a KNP instance.
knp = KNP()  # or `kwja = KWJA()`

# Apply KNP to a sentence.
sent = knp.apply_to_sentence(sys.argv[1])

# Get information.
if sent.is_clause_tag_required() is True:
    print("KNP might be too old; please update it.")
    sys.exit(1)

discourse_relations = []
for clause in sent.clauses:
    discourse_relations.extend(clause.discourse_relations)

if discourse_relations:
    print(f"Found {len(discourse_relations)} discourse relations:")
    for i, discourse_relation in enumerate(discourse_relations, start=1):
        modifier = discourse_relation.modifier
        head = discourse_relation.head
        label = discourse_relation.label
        print(f'  {i}. "{modifier}" -({label.value})-> "{head}"')
else:
    print("No discourse relation found.")
