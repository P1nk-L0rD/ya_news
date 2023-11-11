import pytest


def transform_list(x):
    x.append(1)
    x.extend([2, 3])
    return x


@pytest.mark.skip
def test_list():
    a = []
    a = transform_list(a)
    a = [4] + a
    assert a == [1, 2, 3, 4]
