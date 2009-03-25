Django Resolvetag
==================

Django Resolvetag is an enhanced replacement for Django's builtin ``url``
template tag.

Features
--------

- Consistent syntax ("string literals" and *variables*)
- Ability to resolve view names stored in context variables
- Partial resolving (see *Advanced Usage* below)

Dependencies
------------

Python 2.3+

Installation
------------

TODO: add setup.py

To use resolvetag in your Django project it needs to be accessible by your 
Python installation. The simplest way to achieve that is by putting the 
``resolvetag`` folder into your Python installation's ``site-packages`` 
directory.

Then all that is left to do is adding ``resolvetag`` to ``INSTALLED_APPS`` in 
your projets ``settings.py``. Example::

	INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.sites',
		'django.contrib.admin',
		'resolvetag',                  # <-- add this
		'your.other.app',
	)

Usage
-----

