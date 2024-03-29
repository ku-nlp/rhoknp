# rhoknp: Yet another Python binding for Juman++/KNP/KWJA

[![Test](https://img.shields.io/github/actions/workflow/status/ku-nlp/rhoknp/test.yml?branch=main&logo=github&label=test&style=flat-square)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/github/ku-nlp/rhoknp?logo=codecov&style=flat-square)](https://codecov.io/gh/ku-nlp/rhoknp)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/ku-nlp/rhoknp?style=flat-square)](https://www.codefactor.io/repository/github/ku-nlp/rhoknp)
[![PyPI](https://img.shields.io/pypi/v/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)
[![Documentation](https://img.shields.io/readthedocs/rhoknp?style=flat-square)](https://rhoknp.readthedocs.io/en/latest/?badge=latest)

**rhoknp** is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp), [KNP](https://github.com/ku-nlp/knp), and [KWJA](https://github.com/ku-nlp/kwja).

```python3
import rhoknp

# Perform language analysis by Juman++
jumanpp = rhoknp.Jumanpp()
sentence = jumanpp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")

# Dump language analysis by Juman++
with open("result.jumanpp", "wt") as f:
    f.write(sentence.to_jumanpp())

# Load language analysis by Juman++
with open("result.jumanpp", "rt") as f:
    sentence = rhoknp.Sentence.from_jumanpp(f.read())
```

```{admonition} Why not *pyknp*?
:class: note
[*pyknp*](https://pypi.org/project/pyknp/) has been developed as the official Python binding for Juman++ and KNP.
In *rhoknp*, we redesigned the API from the top-down, taking into account the current use cases of *pyknp*.
The main differences from *pyknp* are as follows:

- **Support document-level language analysis**: *rhoknp* can load and instantiate the result of document-level language analysis: i.e., cohesion analysis and discourse relation analysis.
- **Strictly type-aware**: *rhoknp* is thoroughly annotated with type annotations. Efficient development is possible with the help of an IDE.
- **Extensive test suite**: *rhoknp* is tested with an extensive test suite. See the code coverage at Codecov.
```

```{toctree}
---
hidden:
caption: User Guide
maxdepth: 1
---

installation/index
reference/index
cli/index
format/index
```

```{toctree}
---
hidden:
caption: Development
maxdepth: 1
---

contributing/index
authors
```

```{toctree}
---
hidden:
caption: Project Links
---

GitHub <https://github.com/ku-nlp/rhoknp>
PyPI <https://pypi.org/project/rhoknp/>
```

## Indices and tables

- {ref}`genindex`
- {ref}`search`
