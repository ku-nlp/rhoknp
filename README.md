# rhoknp: Yet another Python binding for Juman++/KNP

[![Run Test](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml/badge.svg)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/ku-nlp/rhoknp/branch/main/graph/badge.svg?token=29S0XMLTRG)](https://codecov.io/gh/ku-nlp/rhoknp)
![License](http://img.shields.io/badge/license-MIT-blue.svg)

`rhoknp` is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp) and [KNP](https://github.com/ku-nlp/knp).

## Requirements
- Juman++ v2.0.0-rc3+
- KNP 5.0+

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
