# Welcome to pytest-tape

Easy assertion with expected results saved to yaml files



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

You can install `pytest-tape` via `pip`:

```
pip install pytest-tape
```

Usage
-----

Just use  `tape` fixture in any of the tests and assert dictionary of results with it.


```python
def test_correctness(tape):
    result_of_calc = {
    'a': [1,2,3], 'b':'Another_Random_Result', 'c': 45.99
    }
    assert tape == result_of_calc
```

First time the tests fails, tape writes to yaml file.
Second and all subsequent times you run the test - it compares the result with what is on tape.
