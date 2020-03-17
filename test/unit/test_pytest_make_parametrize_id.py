# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : test_pytest_make_parametrize_id.py
# @Time : 2020/3/16 14:32
# @Author : Nick
import pytest


@pytest.mark.parametrize(
    'a, b',
    [
        (1, {'Two Scoops of Django': '1.8'}),
        (True, 'Into the Brambles'),
        ('Jason likes cookies', [1, 2, 3]),
    ],
)
@pytest.mark.parametrize(
    'c',
    [
        'hello world',
        123,
    ],
)
def test_foobar(a, b, c):
    assert True



