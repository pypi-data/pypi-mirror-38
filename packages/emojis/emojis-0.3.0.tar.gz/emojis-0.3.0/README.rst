Emojis |Build Status|
=====================

Emojis for Python

About
-----

This library allows you to emojify content such as:
``This is a message with emojis :smile: :heart:``

See the `Emoji cheat sheet <http://www.emoji-cheat-sheet.com/>`__ for
more aliases.

Emoji database based on `gemoji <https://github.com/github/gemoji>`__.

Example
-------

.. code:: python

    >>> import emojis

    >>>  emojis.encode('This is a message with emojis :smile: :heart:')
    'This is a message with emojis 😄 ❤️'

    >>> emojis.decode('This is a message with emojis 😄 ❤️')
    'This is a message with emojis :smile: :heart:'

    >>> emojis.get('Prefix 😄 ❤️ 😄 ❤️ Sufix')
    {'😄', '❤️'}

    >> emojis.count('😄 ❤️ 😄 ❤️')
    4

    >>> emojis.count('😄 ❤️ 😄 ❤️', unique=True)
    2

Installation
------------

Install ``emojis`` with ``pip``.

``pip3 install -U emojis``

License
-------

MIT

.. |Build Status| image:: https://travis-ci.org/alexandrevicenzi/emojis.svg?branch=master
   :target: https://travis-ci.org/alexandrevicenzi/emojis
