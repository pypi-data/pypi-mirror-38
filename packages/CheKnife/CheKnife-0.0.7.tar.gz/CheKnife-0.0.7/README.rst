CheKnife
========

Python utilities compilation.

-  Free software: MIT license

Install
=======

::

    pip install CheKnife

Packages
========

| `CheKnife.pki <docs/CheKnife.choiceutils.md>`__
| `CheKnife.hashing <docs/CheKnife.files.md>`__

Tests
=====

.. code:: bash

    nosetests --with-coverage --cover-inclusive --cover-package=CheKnife --cover-html

Upload to PyPi
==============

.. code:: bash

    python setup.py sdist upload -r pypi
