============
pybd-miniapp
============

Baidu SmartProgram Module for Python for MiniApp.

Installation
============

::

    pip install pybd-miniapp


Usage
=====

::

    from pybd_miniapp import get_session_key, get_userinfo, get_phone_number


Method
======

::

    def get_session_key(self, appid=None, secret=None, code=None, storage=None):

    def get_userinfo(self, appid=None, secret=None, code=None, session_key=None, encryptedData=None, iv=None, storage=None):

    def get_phone_number(self, appid=None, secret=None, code=None, session_key=None, encryptedData=None, iv=None, storage=None):

