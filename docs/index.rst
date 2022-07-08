.. rhoknp documentation master file, created by
   sphinx-quickstart on Fri Oct  1 21:33:49 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rhoknp: Yet another Python binding for Juman++/KNP
==================================================

.. image:: http://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.org/project/rhoknp/
    :alt: License Badge

.. image:: https://img.shields.io/pypi/v/rhoknp.svg
    :target: https://pypi.org/project/rhoknp/
    :alt: Wheel Support Badge

.. image:: https://img.shields.io/pypi/pyversions/rhoknp.svg
    :target: https://pypi.org/project/rhoknp/
    :alt: Python Version Support Badge

**rhoknp** is a Python binding for `Juman++ <https://github.com/ku-nlp/jumanpp>`_ and `KNP <https://github.com/ku-nlp/knp>`_.

.. code-block:: python3

   import rhoknp

   # Perform language analysis by Juman++
   jumanpp = rhoknp.Jumanpp()
   sentence = jumanpp.apply("電気抵抗率は電気の通しにくさを表す物性値である。")

   # Dump language analysis by Juman++
   with open("result.jumanpp", "wt") as f:
       f.write(sentence.to_jumanpp())

   # Load language analysis by Juman++
   with open("result.jumanpp", "rt") as f:
       sentence = rhoknp.Sentence.from_jumanpp(f.read())


.. toctree::
   :maxdepth: 2

   install/index
   reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
