import pytest


class Test_Example:
    def test_pass(self):
        assert 1 == 1

    def test_fail(self):
        assert 0 == 1
