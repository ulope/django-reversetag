=================
Django Reversetag
=================

Django Reversetag is an enhanced replacement for Django's builtin url_
template tag.

.. _url: http://docs.djangoproject.com/en/dev/ref/templates/builtins/#url

--------
Features
--------

- Consistent syntax ("string literals" and *variables*)
- Ability to reverse view names stored in context variables
- Partial reversing (see *Advanced Usage* below)

------------
Dependencies
------------

Python 2.3+

------------
Installation
------------

(TODO: add setup.py)

To use reversetag in your Django project it needs to be accessible by your 
Python installation. The simplest way to achieve that is by putting the
``reversetag`` directory into your Python installation's ``site-packages``
directory.

Then all that is left to do is adding ``reversetag`` to ``INSTALLED_APPS`` in 
your projets ``settings.py``. Example::

	INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.sites',
		'django.contrib.admin',
		'reversetag',                  # <-- add this
		'your.other.app',
	)

-----
Usage
-----

Basic usage is pretty similar to the default ``url`` tag.
Examples::

	{% reverse "app.views.view" %}

	{% reverse "sample_view" %}

This will try to reverse
	a) a view "view" in the app.views module
 	b) a named view "sample_view".

Note that you _must_ quote the view name (regardles if you're using named views or not) since reversetag is "variable aware" and will treat any unquoted view name arguments as template variables and try to reverse them. Example::

	{% reverse next_page_view %}
	
In this example reversetag will look up the template variable ``next_page_view`` and reverse the url to whatever is in stored in that variable.

Arguments
---------

Of course it is also possible to provide arguments 
