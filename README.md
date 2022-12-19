# rhoknp: Yet another Python binding for Juman++/KNP/KWJA

[![Test](https://img.shields.io/github/actions/workflow/status/ku-nlp/rhoknp/test.yml?branch=main&logo=github&label=test&style=flat-square)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/github/ku-nlp/rhoknp?logo=codecov&style=flat-square)](https://codecov.io/gh/ku-nlp/rhoknp)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/ku-nlp/rhoknp?style=flat-square)](https://www.codefactor.io/repository/github/ku-nlp/rhoknp)
[![PyPI](https://img.shields.io/pypi/v/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rhoknp?style=flat-square)
[![Documentation](https://img.shields.io/readthedocs/rhoknp?style=flat-square)](https://rhoknp.readthedocs.io/en/latest/?badge=latest)
[![Code style - black](https://img.shields.io/badge/code%20style-black-222222?style=flat-square)](https://github.com/psf/black)

*rhoknp* is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp), [KNP](https://github.com/ku-nlp/knp), and [KWJA](https://github.com/ku-nlp/kwja).

```python
import rhoknp

# Perform language analysis by Juman++
jumanpp = rhoknp.Jumanpp()
sentence = jumanpp.apply_to_sentence(
    "電気抵抗率は電気の通しにくさを表す物性値である。"
)

# Access to the result
for morpheme in sentence.morphemes:  # a.k.a. keitai-so
    ...

# Save language analysis by Juman++
with open("result.jumanpp", "wt") as f:
    f.write(sentence.to_jumanpp())

# Load language analysis by Juman++
with open("result.jumanpp", "rt") as f:
    sentence = rhoknp.Sentence.from_jumanpp(f.read())
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

Let's start with using Juman++ with *rhoknp*.
Here is a simple example of using Juman++ to analyze a sentence.

```python
# Perform language analysis by Juman++
jumanpp = rhoknp.Jumanpp()
sentence = jumanpp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")
```

You can easily access the morphemes that make up the sentence.

```python
for morpheme in sentence.morphemes:  # a.k.a. keitai-so
    ...
```

Sentence objects can be saved in the JUMAN format.

```python
# Save the sentence in the JUMAN format
with open("sentence.jumanpp", "wt") as f:
    f.write(sentence.to_jumanpp())

# Load the sentence
with open("sentence.jumanpp", "rt") as f:
    sentence = rhoknp.Sentence.from_jumanpp(f.read())
```

Almost the same APIs are available for KNP.

```python
# Perform language analysis by KNP
knp = rhoknp.KNP()
sentence = knp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")
```

KNP performs language analysis at multiple levels.

```python
for clause in sentence.clauses:  # a.k.a., setsu
    ...
for phrase in sentence.phrases:  # a.k.a. bunsetsu
    ...
for base_phrase in sentence.base_phrases:  # a.k.a. kihon-ku
    ...
for morpheme in sentence.morphemes:  # a.k.a. keitai-so
    ...
```

Sentence objects can be saved in the KNP format.

```python
# Save the sentence in the KNP format
with open("sentence.knp", "wt") as f:
    f.write(sentence.to_knp())

# Load the sentence
with open("sentence.knp", "rt") as f:
    sentence = rhoknp.Sentence.from_knp(f.read())
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
# Perform language analysis by Juman++
document = jumanpp.apply_to_document(document)

# Access language units in the document
for sentence in document.sentences:
    ...
for morpheme in document.morphemes:
    ...

# Save language analysis by Juman++
with open("document.jumanpp", "wt") as f:
    f.write(document.to_jumanpp())

# Load language analysis by Juman++
with open("document.jumanpp", "rt") as f:
    document = rhoknp.Document.from_jumanpp(f.read())
```

For more information, explore the [examples](./examples) and [documentation](https://rhoknp.readthedocs.io/en/latest/).

## Main differences from [pyknp](https://github.com/ku-nlp/pyknp/)

[*pyknp*](https://pypi.org/project/pyknp/) has been developed as the official Python binding for Juman++ and KNP.
In *rhoknp*, we redesigned the API from the top-down, taking into account the current use cases of *pyknp*.
The main differences are as follows:

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
