import sys

from rhoknp import Document, Sentence
from rhoknp.utils.reader import Reader

# Read the given file as a list of sentences.
with open(sys.argv[1]) as f:
    reader = Reader(f)
    for jumanpp in reader.read_as_sentences():
        sent = Sentence.from_knp(jumanpp)
        print(f"Successfully loaded a sentence: {sent.text}")

# Read the given file as a list of documents.
with open(sys.argv[1]) as f:
    reader = Reader(f)
    for jumanpp in reader.read_as_documents():
        doc = Document.from_knp(jumanpp)
        print(f"Successfully loaded a document: {doc.text}")
