=============================
dj-dash
=============================

.. image:: https://badge.fury.io/py/dj-dash-repo.svg
    :target: https://badge.fury.io/py/dj-dash-repo

.. image:: https://travis-ci.org/rahul1809/dj-dash-repo.svg?branch=master
    :target: https://travis-ci.org/rahul1809/dj-dash-repo

.. image:: https://codecov.io/gh/rahul1809/dj-dash-repo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rahul1809/dj-dash-repo

This is package for django site analytics

Documentation
-------------

The full documentation is at https://dj-dash-repo.readthedocs.io.

Quickstart
----------

Install dj-dash::

    pip install dj-dash-repo

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dashboard.apps.DashboardConfig',
        ...
    )

Add dj-dash's URL patterns:

.. code-block:: python

    from dashboard import urls as dashboard_urls


    urlpatterns = [
        ...
        url(r'^', include(dashboard_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
