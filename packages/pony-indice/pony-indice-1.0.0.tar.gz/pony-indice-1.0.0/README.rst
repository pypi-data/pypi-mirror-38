===========
Pony Indice
===========

Pony Indice is a Django re-usable app to create a simple search engine for your
project.

Install
=======

Install it as usual (pip coming): ::

    pip install pony-indice
    
Add the app in your ``INSTALLED_APPS``: ::

    INSTALLED_APPS = (
       ...
       'pony_indice',
       ...
    )
    
And launch the migration to create the table: ::

    ./manage.py migrate

Usage
=====

The usage is quite simple: ::

    from pony_indice import registry as indice_registry

    @indice_registry.register()
    class YourModel(models.Models):
       rank = models.IntegerField()

Now your model is tagged as "tracked" and the following behaviors are added:

- On ``post_save`` signals a ``Link`` will be created/updated in database
- On ``post_delete`` the ``Link`` will be mark as "removed"

(Update aren't taken in account and may lead to broken URLs)

Basicaly this app is based on the other decorated models, but you can easily
import ``pony_indice.models.Link`` and add the link which you want, especialy
external ones.

Tools
=====

QuerySet
--------

The ``Link``'s queryset has the method ``filter_q`` method, which is a simple
filter looking if fields ``display`` or ``description`` contain a string.
Useful to create easily any search tool.

Admin
-----

Of course the admin interface is already configured.

REST Framework
--------------

``pony_indice.contrib.rest_framework.serializers.LinkSerializer`` and
``pony_indice.contrib.rest_framework.viewsets.LinkViewsets`` are here to play
quickly with Django REST Framework.