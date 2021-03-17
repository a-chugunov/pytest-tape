# -*- coding: utf-8 -*-
import os

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


def test_no_tape(pytester):

    pytester.makepyfile(test_me="""
        import pytest

        def test_hello_world(tape):
            assert tape == 5.0
    """)

    # first run - fail
    resultFAIL = pytester.runpytest_inprocess('-v')
    assert resultFAIL.ret == 1

def test_tape_ok(pytester, tmpdir):

    pytester.makepyfile(test_me="""
        import pytest

        def test_hello_world(tape):
            assert tape == 5.0
    """)
    os.mkdir(pytester.path.joinpath('tape'))
    tape_path = pytester.path.joinpath('tape', 'test_me.yaml')

    with open(tape_path, 'w') as f:
        f.write(
            """
            test_hello_world:
            - params: None
              results: 5.0
            """
        )

    # run - success
    resultOK = pytester.runpytest_inprocess('-v')
    assert resultOK.ret == 0

def test_tape_fail(pytester, tmpdir):

    pytester.makepyfile(test_me="""
        import pytest

        def test_hello_world(tape):
            assert tape == 5.0
    """)
    os.mkdir(pytester.path.joinpath('tape'))
    tape_path = pytester.path.joinpath('tape', 'test_me.yaml')

    with open(tape_path, 'w') as f:
        f.write(
            """
            test_hello_world:
            - params: None
              results: 8.0
            """
        )

    # run - success
    resultFAIL = pytester.runpytest_inprocess('-v')

    resultFAIL.stdout.fnmatch_lines([
        '*assert 8.0 == 5.0*'
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
