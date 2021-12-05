# rhoknp: Yet another Python binding for Juman++/KNP

[![Run Test](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml/badge.svg)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/ku-nlp/rhoknp/branch/main/graph/badge.svg?token=29S0XMLTRG)](https://codecov.io/gh/ku-nlp/rhoknp)
![License](http://img.shields.io/badge/license-MIT-blue.svg)

`rhoknp` is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp) and [KNP](https://github.com/ku-nlp/knp).

## Requirements
- Juman++ v2.0.0-rc3+
- KNP 5.0+

<!--- uncomment here after publication
## Installation
```shell
pip install rhoknp
```
-->

## Parse a sentence/document

```python
from rhoknp import KNP, Sentence, Document

# Create a KNP instance
knp = KNP()
# Parse the sentence using KNP
sentence: Sentence = knp.apply("電気抵抗率は、電気の通しにくさを表す物性値である。")

# Parse a document
document: Document = knp.apply_to_document("電気抵抗率は、電気の通しにくさを表す物性値である。単に、抵抗率とも呼ばれる。")

# Show the parent of each phrase
for phrase in sentence.phrases:
    print(f"{phrase} -> {phrase.parent}")
```

For more examples, explore the [examples](./examples) directory.

## Differences from [pyknp](https://github.com/ku-nlp/pyknp/tree/master/pyknp)

- *rhoknp* provides APIs for document-level text analysis
- *rhoknp* employs more consistent class names
- *rhoknp* is strictly type-aware, which provides high readability and usability
- *rhoknp* drops a support for Python2 and supports Python3.9+

## Why not [pyknp](https://github.com/ku-nlp/pyknp)?

`pyknp` is the official Python binding that has been developed over a long time.
During its development, features have been added incrementally while keeping the basic design intact.
As a result, the API has become inconsistent.
In addition, unit testing has not been exhaustively conducted.
As a result, ad hoc bug fixes have been repeated.
In short, `pyknp` is now a tool that is difficult to use for users and difficult to maintain for developers.

In `rhoknp`, we redesigned the API from the top-down, taking into account the current use cases of `pyknp`.
What you can do with `rhoknp` can be done with `pyknp`, but using `rhoknp` is often more concise.
The code quality is ensured through exhaustive unit testing and the introduction of a formatter, linter, and static type checker.

## Reference

- [KNP FORMAT](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)
- [KNP - KUROHASHI-CHU-MURAWAKI LAB](https://nlp.ist.i.kyoto-u.ac.jp/?KNP)
