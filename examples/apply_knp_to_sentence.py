from rhoknp import KNP

# Create a KNP instance.
knp = KNP()

# Apply Jumanpp to a sentence.
sent = knp.apply("電気抵抗率は、電気の通しにくさを表す物性値である。")

# Get information.
for mrph in sent.morphemes:
    print(f"Text: {mrph.text}")
    print(f"Reading: {mrph.reading}")
    print(f"Lemma: {mrph.lemma}")
    print(f"POS: {mrph.pos}")
    print(f"Sub-POS: {mrph.subpos}")
    print(f"Conjugation (type): {mrph.conjtype}")
    print(f"Conjugation (form): {mrph.conjform}")
    print("---")
