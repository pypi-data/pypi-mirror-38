=============================
Django Script Codes (ISO 15924)
=============================

.. image:: https://badge.fury.io/py/django-script-codes.svg
    :target: https://badge.fury.io/py/django-script-codes

.. image:: https://travis-ci.org/kingsdigitallab/django-script-codes.svg?branch=master
    :target: https://travis-ci.org/kingsdigitallab/django-script-codes

.. image:: https://codecov.io/gh/kingsdigitallab/django-script-codes/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kingsdigitallab/django-script-codes

Application providing access to the script codes standard ISO 15924.

Documentation
-------------

The full documentation is at https://django-script-codes.readthedocs.io.

Quickstart
----------

Install Django Script Codes (ISO 15924)::

    pip install django-script-codes

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'script_codes.apps.ScriptCodesConfig',
        ...
    )

To reference Script Codes in your models:

.. code-block:: python

    from django.db import models
    from script_codes.models import Script


    class MyModel(models.Model):
        ...
        script = models.ForeignKey(Script, on_delete=models.CASCADE)
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
