axju
====

.. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg
  :alt: Gitter
  :target: https://gitter.im/axju/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link

.. image:: https://img.shields.io/twitter/url/https/github.com/axju/axju.svg?style=social
  :alt: Twitter
  :target: https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Faxju%2Faxju

This small project help me, to automate boring stuff. It started with deploying
django, but where will coming more. Hopefully


Install
-------
::

  pip install axju

Functions
---------
::

  axju
  axju-django


Development
-----------
Clone repo::

  git clone https://github.com/axju/axju.git

Create virtual environment and update dev-tools::

  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade wheel pip setuptools twine tox

Install local::

  pip install -e .

Run some tests::

  tox
  python setup.py test

Make the documentation::

  docs/make.bat html

Publish the packages::

  python setup.py sdist bdist_wheel
  twine upload dist/*
