# -*- coding: utf-8 -*-

import pytest

import os
import atexit
import yaml
import json
import hashlib

@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


def pytest_addoption(parser):
    group = parser.getgroup('tape')
    group.addoption(
        '--tape-rel-tolerance',
        action='store',
        type=float,
        default=None,
        help='Tape relative tolerance.'
    )
    group.addoption(
        '--tape-abs-tolerance',
        action='store',
        type=float,
        default=None,
        help='Tape absolute tolerance.'
    )
    group.addoption(
        '--tape-overwrite',
        action='store_true',
        default=False,
        help='Tape overwrite.'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture(scope='module')
def _tape_class(request):
    class _TapeClass:
        def __init__(self):
            atexit.register(self.cleanup)
            self._test_name = None
            self._test_params = None
            self._test_tape = None
            self._module_tape = {}

            self._folder = os.path.join(request.fspath.dirname, 'tape')
            self._filename = os.path.join(self._folder, f'{request.module.__name__}.yaml')

            self.rel_tolerance = request.config.getoption('--tape-rel-tolerance')
            self.abs_tolerance = request.config.getoption('--tape-abs-tolerance')

            self.overwrite_tape = request.config.getoption('--tape-overwrite')

            # Create directory if does not exist
            if not os.path.exists(self._folder):
                os.mkdir(self._folder)

            # Load existing tape into dictionary
            if os.path.exists(self._filename):
                with open(self._filename) as f:
                    self._module_tape = yaml.safe_load(f) or {}


        def cleanup(self):
            # On delete we want to save all results
            self._write_tape()

        def __repr__(self):
            return str(self._test_tape)

        def _write_tape(self):
            with open(self._filename, 'w') as f:
                yaml.SafeDumper.ignore_aliases = lambda *args: True
                yaml.safe_dump(self._module_tape, f)

        def _add_to_tape(self, test_results):
            self._module_tape[self._test_name].append({
                'params': self._test_params,
                'results': test_results
            })

        def get_tape(self, name, params):
            self._test_name = name
            self._test_params = {}

            for key, value in params.items():
                self._test_params[key] = str(value)

            if self._test_params == {}:
                self._test_params = 'None'
            else:
                self._test_params = hashlib.sha224(
                        json.dumps(self._test_params, sort_keys=True)
                    ).hexdigest()

            if self._test_name not in self._module_tape.keys():
                self._module_tape.update({ self._test_name: [] })

            # check if results with exact same params exist on tape
            test_tape_list = [
                d['results'] for d in self._module_tape[self._test_name]
                if d['params'] == self._test_params
            ]

            if len(test_tape_list) == 1:
                self._test_tape = test_tape_list[0]
            elif  len(test_tape_list) == 0:
                self._test_tape = None
            else:
                assert 0, 'Suplicate results in file - please clean it'


            return self

        def __eq__(self, other):
            """
            Compare results if they are available in file, else store them.

            :param other: results against which we're comparing
            :return:
            """

            # if no result - save in yaml and FAIL the test
            if (self._test_tape is None) or self.overwrite_tape:
                self._add_to_tape(other)
                self._write_tape()
                return False

            # compare with available result
            if not (self.rel_tolerance or self.abs_tolerance):
                return other == self._test_tape

            # pytest approx if we're using tolerance
            if type(self._test_tape) is dict:
                for key, value in self._test_tape.items():
                    if other[key] != pytest.approx(value,
                                                   rel=self.rel_tolerance,
                                                   abs=self.abs_tolerance
                                                   ):
                        return False
                return True
            else:
                return other == pytest.approx(self._test_tape,
                                              rel=self.rel_tolerance,
                                              abs=self.abs_tolerance
                                              )

    return _TapeClass()


@pytest.fixture(scope='function')
def tape(request, _tape_class):
    name = request.node.originalname or request.node.originalname
    params = request.node.funcargs.copy()
    for key in ['request', 'tape', '_tape_class']:
        params.pop(key, None)
    return _tape_class.get_tape(name, params)
