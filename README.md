# rhoknp: Yet another Python binding for Juman++/KNP/KWJA

[![Test](https://img.shields.io/github/workflow/status/ku-nlp/rhoknp/test?logo=github&label=test&style=flat-square)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/github/ku-nlp/rhoknp?logo=codecov&style=flat-square)](https://codecov.io/gh/ku-nlp/rhoknp)
[![PyPI](https://img.shields.io/pypi/v/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rhoknp?style=flat-square)
[![Documentation](https://img.shields.io/readthedocs/rhoknp?style=flat-square)](https://rhoknp.readthedocs.io/en/latest/?badge=latest)
[![Code style - black](https://img.shields.io/badge/code%20style-black-222222?style=flat-square)](https://github.com/psf/black)

*rhoknp* is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp), [KNP](https://github.com/ku-nlp/knp), and [KWJA](https://github.com/ku-nlp/kwja).

```python
import rhoknp

# Perform language analysis by Juman++
jumanpp = rhoknp.Jumanpp()
sentence = jumanpp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")

# Save language analysis by Juman++
with open("result.jumanpp", "wt") as f:
    f.write(sentence.to_jumanpp())

# Load language analysis by Juman++
with open("result.jumanpp", "rt") as f:
    sentence = rhoknp.Sentence.from_jumanpp(f.read())

# Perform language analysis by KNP
knp = rhoknp.KNP()
sentence = knp.apply_to_sentence(sentence)  # or knp.apply_to_sentence("電気抵抗率は...")

# Save language analysis by KNP
with open("result.knp", "wt") as f:
    f.write(sentence.to_knp())

# Load language analysis by KNP
with open("result.knp", "rt") as f:
    sentence = rhoknp.Sentence.from_knp(f.read())

# Perform language analysis by KWJA
kwja = rhoknp.KWJA()
sentence = kwja.apply_to_sentence(sentence)  # or kwja.apply_to_sentence("電気抵抗率は...")
```

## Requirements

- Python 3.8+

## Optional requirements for language analysis

- [Juman++](https://github.com/ku-nlp/jumanpp) v2.0.0-rc3+
- [KNP](https://github.com/ku-nlp/knp) 5.0+
- [KWJA](https://github.com/ku-nlp/kwja) 1.0.0+

## Installation

```shell
pip install rhoknp
```

## Documentation

[https://rhoknp.readthedocs.io/en/latest/](https://rhoknp.readthedocs.io/en/latest/)

## Quick tour

*rhoknp* provides APIs to perform language analysis by Juman++ and KNP.

```python
# Perform language analysis by Juman++
jumanpp = rhoknp.Jumanpp()
sentence = jumanpp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")

# Perform language analysis by KNP
knp = rhoknp.KNP()
sentence = knp.apply_to_sentence(sentence)  # or knp.apply_to_sentence("電気抵抗率は...")
```

Sentence objects can be saved in the Juman/KNP format

```python
# Save language analysis by Juman++
with open("result.jumanpp", "wt") as f:
    f.write(sentence.to_jumanpp())

# Save language analysis by KNP
with open("result.knp", "wt") as f:
    f.write(sentence.to_knp())
```

and recovered from Juman/KNP-format text.

```python
# Load language analysis by Juman++
with open("result.jumanpp", "rt") as f:
    sentence = rhoknp.Sentence.from_jumanpp(f.read())

# Perform language analysis by KNP
with open("result.knp", "rt") as f:
    sentence = rhoknp.Sentence.from_knp(f.read())
```

It is easy to access the linguistic units that make up a sentence.

```python
for clause in sentence.clauses:
    ...
for phrase in sentence.phrases:  # a.k.a. bunsetsu
    ...
for base_phrase in sentence.base_phrases:  # a.k.a. kihon-ku
    ...
for morpheme in sentence.morphemes:
    ...
```

*rhoknp* also provides APIs for document-level language analysis.

```python
document = rhoknp.Document.from_raw_text(
    "電気抵抗率は電気の通しにくさを表す物性値である。単に抵抗率とも呼ばれる。"
)
# If you know sentence boundaries, you can use `Document.from_sentences` instead.
document = rhoknp.Document.from_sentences(
    [
        "電気抵抗率は電気の通しにくさを表す物性値である。",
        "単に抵抗率とも呼ばれる。",
    ]
)
```

Document objects can be handled in almost the same way as Sentence objects.

```python
# Perform language analysis by Juman++/KNP
document = jumanpp.apply_to_document(document)
document = knp.apply_to_document(document)

# Save language analysis by Juman++/KNP
with open("result.jumanpp", "wt") as f:
    f.write(document.to_jumanpp())
with open("result.knp", "wt") as f:
    f.write(document.to_knp())

# Load language analysis by Juman++/KNP
with open("result.jumanpp", "rt") as f:
    document = rhoknp.Document.from_jumanpp(f.read())
with open("result.knp", "rt") as f:
    document = rhoknp.Document.from_knp(f.read())

# Access language units in the document
for sentence in document.sentences:
    ...
for clause in document.clauses:
    ...
for phrase in document.phrases:
    ...
for base_phrase in document.base_phrases:
    ...
for morpheme in document.morphemes:
    ...
```

For more information, explore the [examples](./examples) and [documentation](https://rhoknp.readthedocs.io/en/latest/).

## Main differences from [pyknp](https://github.com/ku-nlp/pyknp/)

- **Support for document-level language analysis**: *rhoknp* can load and instantiate the result of document-level language analysis (i.e., cohesion analysis and discourse relation analysis).
- **Strictly type-aware**: *rhoknp* is thoroughly annotated with type annotations.
- **Extensive test suite**: *rhoknp* is tested with an extensive test suite. See the code coverage at [Codecov](https://app.codecov.io/gh/ku-nlp/rhoknp).

## License

MIT

## Contributing

We welcome contributions to *rhoknp*.
You can get started by reading the [contribution guide](https://rhoknp.readthedocs.io/en/latest/contributing/index.html).

## Reference

- [KNP FORMAT](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)
- [KNP - KUROHASHI-CHU-MURAWAKI LAB](https://nlp.ist.i.kyoto-u.ac.jp/?KNP)
