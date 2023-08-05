.. -*- mode: rst -*-

|Travis|_ |PyPi|_ |TestStatus|_ |PythonVersion|_

.. |Travis| image:: https://travis-ci.org/aagnone3/auto-proto.svg?branch=master
.. _Travis: https://travis-ci.org/aagnone3/auto-proto

.. |PyPi| image:: https://badge.fury.io/py/auto-proto.svg
.. _PyPi: https://badge.fury.io/py/auto-proto

.. |TestStatus| image:: https://travis-ci.org/aagnone3/auto-proto.svg
.. _TestStatus: https://travis-ci.org/aagnone3/auto-proto.svg

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/auto-proto.svg
.. _PythonVersion: https://img.shields.io/pypi/pyversions/auto-proto.svg

auto-proto
================

auto-proto is a python package offering automated protocol buffer generation from
examples of the data that you wish to model.

Documentation
-------------

Documentation can be found at the github pages here_

.. _here: https://aagnone3.github.io/auto-proto/

Dependencies
~~~~~~~~~~~~

auto-proto is tested to work under Python 3.x.
See the requirements via the following command:

.. code-block:: bash

  cat requirements.txt

Installation
~~~~~~~~~~~~

auto-proto is currently available on the PyPi's repository and you can
install it via `pip`:

.. code-block:: bash

  pip install -U auto-proto

If you prefer, you can clone it and run the setup.py file. Use the following
commands to get a copy from GitHub and install all dependencies:

.. code-block:: bash

  git clone https://github.com/aagnone3/auto-proto.git
  cd auto-proto
  pip install .

Or install using pip and GitHub:

.. code-block:: bash

  pip install -U git+https://github.com/aagnone3/auto-proto.git

Testing
~~~~~~~

.. code-block:: bash

  make test
  
