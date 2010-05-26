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

To use reversetag in your Django project it needs to be accessible by your 
Python installation. 

The easy way:

	#~ pip install django-reversetag
	(or use *easy_install* if you must)

The manual way:

Simply place the ``reversetag`` directory somewhere that is on your 
$PYTHONPATH.


Django Setup
------------

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

Note that you _must_ quote the view name (regardles if you're using named
views or not) since reversetag is "variable aware" and will treat any unquoted
view name arguments as template variables and try to reverse them. Example::

	{% reverse next_page_view %}

In this example reversetag will look up the template variable
``next_page_view`` and reverse the url to whatever is in stored in that
variable.

Arguments
---------

Of course it is also possible to provide arguments for views that require
them. Example::

	{% reverse "sample_view" "arg1","arg2" %}

	{% reverse "sample_view" arg1_var,arg2_var %}

	{% reverse "sample_view" key1="arg1",key2="arg2" %}

	{% reverse "sample_view" key1=arg1_var,key2=arg2_var %}

As with the view name literal arguments have to be quoted, otherwise they
will be treated as variables. 

Note: Since Django's``reverse`` method does not permit mixing args and kwargs
reversetag does not allow this as well.

Saving the result
-----------------

If you want to use the reversed url in multiple places you can save the result
in a context variable. Example::

	{% reverse "sample_view" "arg1" as my_url %}

--------------
Advanced usage
--------------

There is also a more advanced mode of operation called partial reversing. What
this does is allow you to reverse views that require arguments in multiple
steps.

This is useful in situations where you want to use a generic template (e.g.
list pagination) that needs to construct urls to a page with an additional
parameter(s) without beeing hardcoded to a specific view (e.g. a page number).
The "normal" way of doing this is using GET parameters, but GET parameters
adversely affect caching [1]_, are bad for search
engines and just looks ugly.

.. [1] If you're using Django's Cache Middleware it *completely skips* caching
   for pages with GET parameters!

Example::

	- urls.py -
	...
	url(r'^something/(?P<page>[0-9]+)', 'app.views.view', name="paginatable_view"),
	...
	- /urls.py -
	
	- template.html -
	{% reverse partial "paginatable_view" as this_page %}
	{% include pagination.html %}
	- /template.html -
	
	- pagination.html -
	<a href="{% reverse this_page page=2 %}">next page</a>
	- /pagination.html -

In this example the template ``template.html`` constructs a partial reversed
url to itself and saves the result in a context varialbe ``this_page`` which
in turn is used by a generic ``pagination.html`` to display a link to the next
page without having to know anything about the view except that it takes a
``page`` argument.

