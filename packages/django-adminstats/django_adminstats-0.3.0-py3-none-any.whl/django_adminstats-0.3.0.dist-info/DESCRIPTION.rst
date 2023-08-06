==================
Django Admin Stats
==================

|pipeline-badge| |coverage-badge| |pypi-badge|

Django Admin Stats allows you to create and display charts of your data
using the django admin. It uses `c3 <https://c3js.org/>`_ to display charts.

Features
--------

* Supports generating statistics from django models and from trackstats_
  metrics.
* Also allows for custom statistics generation by making your own
  ``Registration`` subclass.
* Nice JavaScript charts with c3, falls back to a plain table without
  JavaScript.

Limitations
-----------

* One dimension/axis of the chart is always the date. There's no way to
  specify a chart that isn’t “by date”.
* There’s no way to add filters to criteria on charts. The recommended
  workaround is to use trackstats and store those stats separately.

Installation
------------

Installation is straightforward. Install ``django-adminstats`` with pip, and
then add ``'django_adminstats',`` to your ``INSTALLED_APPS`` setting. You’ll
also want to register some models or trackstat metrics (see Example Code).

Example Code
------------

See ``tests/models.py``.

Demo
----

Just run ``make demo`` and log in with user ``admin`` and password ``admin``.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/django-adminstats/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/django-adminstats/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/django-adminstats/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/django-adminstats/
   :alt: Coverage Status

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django_adminstats.svg
   :target: https://pypi.org/project/django-adminstats/
   :alt: Project on PyPI

.. _trackstats: https://pypi.org/project/django-trackstats/



