BosonNLP Python SDK
======================

BosonNLP HTTP API 封装库（SDK）。

安装
----

`bosonnlp` 代码托管在 `GitHub`_，并且已经发布到 `PyPI`_，可以直接通过 `pip` 安装::

    $ pip install bosonnlp

`bosonnlp` 以 MIT 协议发布。

.. _GitHub: https://github.com/bosondata/bosonnlp.py
.. _PyPI: https://pypi.python.org/pypi/bosonnlp

使用教程
--------

    >>> from bosonnlp import BosonNLP
    >>> nlp = BosonNLP('YOUR_API_TOKEN')
    >>> nlp.sentiment('这家味道还不错')
    [[0.8758192096636473, 0.12418079033635264]]

SDK API 文档地址：http://bosonnlp-py.readthedocs.org/

可以在 `BosonNLP`_ 文档站点阅读详细的 BosonNLP HTTP API 文档。

.. _BosonNLP: http://docs.bosonnlp.com/
