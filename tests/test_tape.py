# -*- coding: utf-8 -*-

def test_help_message(pytester):
    result = pytester.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'tape:',
        '*--tape-rel-tolerance=TAPE_REL_TOLERANCE*',
        '*Tape relative tolerance.*',
        '*--tape-abs-tolerance=TAPE_ABS_TOLERANCE*',
        '*Tape absolute tolerance.*',
        '*--tape-overwrite*Tape overwrite.*',
    ])

def test_very_simple():
    assert 0 == 0, 'well, this should work'

def test_tape_simple(pytester, tmpdir):

    pytester.makepyfile("""
        import pytest

        def test_hello_world(tape):
            assert tape == 5.0
    """)

    # first run - fail
    resultFAIL = pytester.runpytest('-v')
    resultFAIL.stdout.fnmatch_lines([
        '*FAILED test_tape_simple.py::test_hello_world*'
    ])
    assert resultFAIL.ret == 1

    # second run - success
    resultOK = pytester.runpytest('-v')
    resultOK.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*'
    ])

    assert resultOK.ret == 0

    pytester.makepyfile("""
        import pytest

        def test_hello_world(tape):
            assert tape == 7.0
    """)
    resultFAIL = pytester.runpytest('-v')
    resultFAIL.stdout.fnmatch_lines([
        '*FAILED test_tape_simple.py::test_hello_world*'
    ])
    assert resultFAIL.ret == 1



def test_hello_ini_setting(pytester):
    pytester.makeini("""
        [pytest]
        HELLO = world
    """)

    pytester.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = pytester.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
