# rhoknp: Yet another Python binding for Juman++/KNP

[![License Badge](http://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.org/project/rhoknp/)
[![Wheel Support Badge](https://img.shields.io/pypi/v/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)
[![Python Version Support Badge](https://img.shields.io/pypi/pyversions/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)

**rhoknp** is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp) and [KNP](https://github.com/ku-nlp/knp).

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
