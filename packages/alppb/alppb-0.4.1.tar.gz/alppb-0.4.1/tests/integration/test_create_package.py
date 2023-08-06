import sys
from unittest.mock import patch
import pytest
from alppb.alppb import main


def test_creating_default_package_with_valid_input():
    testargs = ["alppb", "mlbgame", "rebukethe.net"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_creating_default_package_with_bad_bucket():
    testargs = ["alppb", "mlbgame", "123sdblahalppbdf213"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_creating_python27_package_with_valid_input():
    testargs = ["alppb", "mlbgame", "rebukethe.net", "--python", "2.7"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_creating_python27_package_with_bad_bucket():
    testargs = ["alppb", "mlbgame", "123sdblahalppbdf213", "--python", "2.7"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_creating_python36_package_with_valid_input():
    testargs = ["alppb", "mlbgame", "rebukethe.net", "--python", "3.6"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_creating_python36_package_with_bad_bucket():
    testargs = ["alppb", "mlbgame", "123sdblahalppbdf213", "--python", "3.6"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_creating_python37_package_with_valid_input():
    testargs = ["alppb", "mlbgame", "rebukethe.net", "--python", "3.7"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_creating_python37_package_with_bad_bucket():
    testargs = ["alppb", "mlbgame", "123sdblahalppbdf213", "--python", "3.7"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
