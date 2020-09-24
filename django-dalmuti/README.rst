=======
dalmuti
=======

Dalmuti is a Django app to conduct Web-based board-game. For each users
 can create and play game.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "dalmuti" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dalmuti',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('dalmuti/', include('dalmuti.urls')),

3. Run ``python manage.py migrate`` to create the dalmuti models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/dalmuti/ to participate in the dalmuti.