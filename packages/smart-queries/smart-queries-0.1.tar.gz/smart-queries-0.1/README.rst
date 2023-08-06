=====
Repeat Queries
=====

Smart Queries is a django package which helps django developer to avoid the N+1 queries issue by recording it and keeping a track of it per request.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'repeat_queries',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('repeat_queries/', include('repeat_queries.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server, Hit any endpoint/view and visit http://127.0.0.1:8000/admin/ to see your data.

