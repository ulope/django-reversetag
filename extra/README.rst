django-pagination Patch
=======================

This patch adds support for reversetag to django-pagination_. This means it
will produce nice URLs without query-string cruft.

.. _django-pagination: http://code.google.com/p/django-pagination/

Usage
-----

Apply the patch to your local version of django-pagination.
::

	~/django-pagination # patch -p0 < ~/reversetag-django-pagination.diff

Then you can use reversetag with pagination as follows::

	... your list goes here ...
	{% reverse partial "name_of_your_view" as pagination_view %}
	{% paginate %}

Note: The context variable has to be named ``pagination_view``. Also your view
must accept a parameter named "page" (this automatically works for generic
views).

