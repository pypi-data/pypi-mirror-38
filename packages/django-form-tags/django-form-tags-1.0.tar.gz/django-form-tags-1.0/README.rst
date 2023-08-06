Django form tags
================

.. image:: https://badge.fury.io/py/django-form-tags.png
    :target: https://badge.fury.io/py/django-form-tags

Django templatetags to easily render fieldholders, fieldwrappers and fields.

Documentation
+++++++++++++

The full documentation is at https://django-form-tags.readthedocs.org.

Installation
++++++++++++

.. code-block:: sh

    pip install django-form-tags


Usage
+++++

.. code-block:: python

        INSTALLED_APPS = (
            # ...
            'form_tags',
            # ...
        )


.. code-block:: html

    {% load forms %}
