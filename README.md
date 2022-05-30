# rhoknp: Yet another Python binding for Juman++/KNP

[![Test](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml/badge.svg)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/ku-nlp/rhoknp/branch/main/graph/badge.svg?token=29S0XMLTRG)](https://codecov.io/gh/ku-nlp/rhoknp)
![License](http://img.shields.io/badge/license-MIT-blue.svg)
[![Documentation](https://readthedocs.org/projects/rhoknp/badge/?version=latest)](https://rhoknp.readthedocs.io/en/latest/?badge=latest)

`rhoknp` is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp) and [KNP](https://github.com/ku-nlp/knp).

## Requirements

- Juman++ v2.0.0-rc3+
- KNP 5.0+

## Installation

```shell
pip install rhoknp
```

## Documentation

[https://rhoknp.readthedocs.io/en/latest/](https://rhoknp.readthedocs.io/en/latest/)

## Examples

Explore the [examples](./examples) directory.

## Differences from [pyknp](https://github.com/ku-nlp/pyknp/)

- Provide APIs for document-level text processing
- Employ consistent class names
- Strictly type-aware, which provides high readability and usability
- Drop a support for Python2 and supports Python3.9+

## Reference

- [KNP FORMAT](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)
- [KNP - KUROHASHI-CHU-MURAWAKI LAB](https://nlp.ist.i.kyoto-u.ac.jp/?KNP)
