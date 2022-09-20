from rhoknp import KNP, Document

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

# Apply KNP to a document.
# By default, the document is split into sentences by a regex-based rule.
doc = knp.apply_to_document("電気抵抗率は、電気の通しにくさを表す物性値である。単に、抵抗率とも呼ばれる。")

# If you'd like to split the document into sentences by yourself,
# create a Document instance from a list of sentences, and then apply KNP to it.
doc = Document.from_sentences(["電気抵抗率は、電気の通しにくさを表す物性値である。", "単に、抵抗率とも呼ばれる。"])
doc = knp.apply_to_document(doc)

# Get information.
for sent in doc.sentences:
    for mrph in sent.morphemes:
        print(f"Text: {mrph.text}")
        print(f"Reading: {mrph.reading}")
        print(f"Lemma: {mrph.lemma}")
        print(f"POS: {mrph.pos}")
        print(f"Sub-POS: {mrph.subpos}")
        print(f"Conjugation (type): {mrph.conjtype}")
        print(f"Conjugation (form): {mrph.conjform}")
        print("---")
