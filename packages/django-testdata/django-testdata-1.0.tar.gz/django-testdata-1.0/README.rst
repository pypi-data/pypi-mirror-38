django-testdata
===============

.. image:: https://img.shields.io/pypi/l/django-testdata.svg?style=flat
    :target: https://pypi.python.org/pypi/django-testdata/
    :alt: License

.. image:: https://img.shields.io/pypi/v/django-testdata.svg?style=flat
    :target: https://pypi.python.org/pypi/django-testdata/
    :alt: Latest Version

.. image:: https://travis-ci.org/charettes/django-testdata.svg?branch=master
    :target: https://travis-ci.org/charettes/django-testdata
    :alt: Build Status

.. image:: https://coveralls.io/repos/charettes/django-testdata/badge.svg?branch=master
    :target: https://coveralls.io/r/charettes/django-testdata?branch=master
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/pyversions/django-testdata.svg?style=flat
    :target: https://pypi.python.org/pypi/django-testdata/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/wheel/django-testdata.svg?style=flat
    :target: https://pypi.python.org/pypi/django-testdata/
    :alt: Wheel Status

Django application providing isolation for model instances created during
`setUpTestData`.

Installation
------------

.. code:: sh

    pip install django-testdata

Motivation
----------

Django 1.8 introduced ``TestCase.setUpTestData`` to allow costly generation of
model fixtures to be executed only once per test class in order to speed up
testcase instances execution.

One gotcha of ``setUpTestData`` though is that test instances all share the same
model instances and have to be careful not to alter them to prevent breaking
test isolation. Per Django's `documentation`_::

    Be careful not to modify any objects created in setUpTestData() in your
    test methods. Modifications to in-memory objects from setup work done at
    the class level will persist between test methods. If you do need to modify
    them, you could reload them in the setUp() method with refresh_from_db(),
    for example.

Reloading objects in ``setUp()`` certainly works but it kind of defeats the
purpose of avoiding database hits to speed up tests execution in the first
place. It makes little sense to fetch model instances from the database
given all 

This package offers a different alternative to work around this quirk of
``setUpTestData``. Instead of reloading objects from the database the model
instances assigned as class attributes during ``setUpTestData`` are lazily deep
copied on testcase instance accesses from their original definition. All of
deep copying is done by sharing a `memo`_ which makes sure in-memory relationships
between objects is preserved.

.. _documentation: https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.TestCase.setUpTestData
.. _memo: https://docs.python.org/3/library/copy.html?highlight=memo#copy.deepcopy

Usage
-----

The test data can be either wrapped manually by using ``testdata``.

.. code:: python

    from django.test import TestCase
    from testdata import testdata

    from .models import Author, Book

    class BookTests(TestCase):
        @classmethod
        def setUpTestData(cls):
            cls.author = testdata(Author.objects.create(
                name='Milan Kundera',
            ))
            cls.book = testdata(cls.author.books.create(
                title='Nesnesitelná lehkost bytí',
            ))

Or automatically by using the ``wrap_testdata`` decorator.

.. code:: python

    from django.test import TestCase
    from testdata import testdata

    from .models import Author, Book

    class BookTests(TestCase):
        @classmethod
        @wrap_testdata
        def setUpTestData(cls):
            cls.author = Author.objects.create(
                name='Milan Kundera',
            )
            cls.book = cls.author.books.create(
                title='Nesnesitelná lehkost bytí',
            )

Under the hood ``wrap_testdata`` simply wraps all attributes added to `cls`
during the execution of ``setUpTestData()`` into ``testdata(attr, name=name)``
which has also the nice side effect of speeding subsequent accesses.

Once test data is wrapped the testcase instances methods can alter objects
retrieved from ``self`` without worrying about cross-tests isolation.

.. code:: python

    from django.test import TestCase
    from testdata import testdata

    from .models import Author, Book

    class BookTests(TestCase):
        @classmethod
        @wrap_testdata
        def setUpTestData(cls):
            cls.author = Author.objects.create(
                name='Milan Kundera',
            )
            cls.book = cls.author.books.create(
                title='Nesnesitelná lehkost bytí',
            )

        def test_book_name_english(self):
            self.assertEqual(self.book.title, 'Nesnesitelná lehkost bytí')
            self.book.title = 'The Unbearable Lightness of Being'
            self.book.save()

        def test_book_name_french(self):
            self.assertEqual(self.book.title, 'Nesnesitelná lehkost bytí')
            self.book.title = "L'Insoutenable Légèreté de l'être"
            self.book.save()
