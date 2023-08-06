import pytest
from math import inf

from linearCounter import LC

def test_add():
    x = LC({"a": 10, "b": 30})
    y = x + 2
    assert y['a'] == 12
    assert y['b'] == 32

def test_sub():
    x = LC({"a": 10, "b": 30})
    y = x - 3
    assert y['a'] == 7
    assert y['b'] == 27

def test_linear():
    x = LC({"a": 10, "b": 30})
    y = LC({"a": 12, "c": 320})
    # the problem with this addition, is that it does not commute.
    # so what?
    z = x + y*3 + 5
    assert z['a'] == 51
    assert z['b'] == 35
    assert z['c'] == 965
    z = x + 5 + y*3
    assert z['a'] == 51
    assert z['b'] == 35
    assert z['c'] == 960

def test_adding_wrong_thing():
    x = LC({"a": 10, "b": 30})
    with pytest.raises(TypeError):
        z = x + "a"
    with pytest.raises(TypeError):
        z = "a" + x

def test_zero():
    x = LC({"a": 10, "b": 30})
    assert len(x/inf) == 0
    assert len(x*0) == 0
    assert len(0*x) == 0
    x['a'] -= 10
    assert 'a' not in x