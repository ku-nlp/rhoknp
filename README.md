# rhoknp: Yet another Python binding for Juman++/KNP

[![Run Test](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml/badge.svg)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/ku-nlp/rhoknp/branch/main/graph/badge.svg?token=29S0XMLTRG)](https://codecov.io/gh/ku-nlp/rhoknp)
![License](http://img.shields.io/badge/license-MIT-blue.svg)

`rhoknp` is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp) and [KNP](https://github.com/ku-nlp/knp).

## Requirements

- Juman++ v2.0.0-rc3+
- KNP 5.0+

## Installation

```shell
pip install rhoknp
```

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
for phrase in sentence.base_phrases:
    print(f"{phrase} -> {phrase.parent}")
```

For more examples, explore the [examples](./examples) directory.

## Differences from [pyknp](https://github.com/ku-nlp/pyknp/)

- Provide APIs for document-level text processing
- Employ consistent class names
- Strictly type-aware, which provides high readability and usability
- Drop a support for Python2 and supports Python3.9+

## Reference

- [KNP FORMAT](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)
- [KNP - KUROHASHI-CHU-MURAWAKI LAB](https://nlp.ist.i.kyoto-u.ac.jp/?KNP)
