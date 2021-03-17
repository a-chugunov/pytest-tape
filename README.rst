===========
pytest-tape
===========

.. image:: https://img.shields.io/pypi/v/pytest-tape.svg
    :target: https://pypi.org/project/pytest-tape
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-tape.svg
    :target: https://test.pypi.org/project/pytest-tape
    :alt: Python versions

.. image:: https://travis-ci.org/a-chugunov/pytest-tape.svg?branch=master
    :target: https://travis-ci.org/a-chugunov/pytest-tape
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/a-chugunov/pytest-tape?branch=master
    :target: https://ci.appveyor.com/project/a-chugunov/pytest-tape/branch/master
    :alt: See Build Status on AppVeyor

Easy assertion with expected results saved to yaml files.



Features
--------

* Creates yaml files for expected test results , a.k.a. tape.
* Creates separate tape for each test file. Each tape stores results for all tests that have utilised tape fixture.
* supports parametrized tests, as long as all parameters can be jsonified.
* Hash functions are used to store and identify params.
* Expected results are stored as dictionaries in yaml, so that they can be compared using tolerances.

Requirements
------------

* python >= 3.6


Installation
------------

You can install "pytest-tape" via `pip`_ from `PyPI`_::

    $ pip install pytest-tape


Usage
-----

Just use  :code:`tape` fixture in any of the tests and assert dictionary of results with it.

.. code-block:: python

    def test_correctness(tape):
        result_of_calc = {
        'a': [1,2,3], 'b':'Another_Random_Result', 'c': 45.99
        }
        assert tape == result_of_calc

First time the tests fails, tape writes to yaml file.
Second and all subsequent times you run the test - it compares the result with what is on tape.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-tape" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.



Acknowledgments
---------------

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/a-chugunov/pytest-tape/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
