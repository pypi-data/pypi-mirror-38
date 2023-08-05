import pytest

from ihan import eprint

def test_eprint():
    eprint('Test')
    assert 1 == 1