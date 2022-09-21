import sys

from rhoknp import Document, Sentence
from rhoknp.utils.reader import chunk_by_document, chunk_by_sentence

# Read the given file as a list of sentences.
with open(sys.argv[1]) as f:
    for knp in chunk_by_sentence(f):
        sent = Sentence.from_knp(knp)
        print(f"Successfully loaded a sentence: {sent.text}")

# Read the given file as a list of documents.
with open(sys.argv[1]) as f:
    for knp in chunk_by_document(f):
        doc = Document.from_knp(knp)
        print(f"Successfully loaded a document: {doc.text}")
