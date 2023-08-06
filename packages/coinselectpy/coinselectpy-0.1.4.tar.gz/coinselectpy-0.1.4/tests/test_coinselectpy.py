#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coinselectpy` package."""

import pytest
# import sys
# import os
# sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

from coinselectpy import coinSelect
from coinselectpy import utils
from coinselectpy import split
from .coin_select_fixture import coin_select
from .test_util import expand


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_utils():
    """Test the utils module."""
    assert utils.inputBytes({}) == 148
    assert utils.outputBytes({}) == 34
    assert utils.dustThreshold({}, 1) == 148
    assert utils.transactionBytes([{}], [{}, {}]) == 226
    assert utils.finalize([{'value': 10000000}], [{}], 1)['fee'] == 226
    assert utils.finalize([{'value': 10000000}], [{}], 1.5)['fee'] == 339


def test_split():
    """Test the split module."""
    assert split.split([{'value': 10000000}], [{}, {}], 1.5) == {
        'fee': 340,
        'inputs': [{'value': 10000000}],
        'outputs': [{'value': 4999830}, {'value': 4999830}]
    }


def test_coin_select(coin_select):
    inputs = expand(coin_select['inputs'], True)
    outputs = expand(coin_select['outputs'])
    # print(inputs, outputs)
    res = coinSelect(inputs, outputs, coin_select['feeRate'])
    assert res == coin_select['expected']
