import pytest
from packages import CRB_Functions as CRB


def funky():
    return 5*5


def test_funky():
    assert funky() == 40


