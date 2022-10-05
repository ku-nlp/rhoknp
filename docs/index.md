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

## Contents

```{toctree}
---
maxdepth: 3
---

install/index
reference/index
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
