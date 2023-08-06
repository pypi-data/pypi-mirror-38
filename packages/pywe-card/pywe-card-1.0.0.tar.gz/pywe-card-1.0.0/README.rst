=========
pywe-card
=========

Wechat Card Module for Python.

Installation
============

::

    pip install pywe-card


Usage
=====

::

    from pywe_card import Card, card_create, card_update


Method
======

::

    class Card(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(Card, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def create(self, data, appid=None, secret=None, token=None, storage=None):

    def update(self, data, appid=None, secret=None, token=None, storage=None):

