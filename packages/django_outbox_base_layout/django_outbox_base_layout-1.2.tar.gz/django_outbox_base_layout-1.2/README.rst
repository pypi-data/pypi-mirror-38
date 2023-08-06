=====
Outbox Base Layout
=====

Outbox Base Layout is a simple Django app with a base layout for new
projects of Outbox Company. The app implements the sbadmin2 template
for Django projects.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "outbox_base_layout" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'outbox_base_layout',
    ]

2. Include the base layout examples URLconf in your project urls.py like this::

    path('examples/', include('outbox_base_layout.urls')),

3. Start the development server and visit http://127.0.0.1:8000/examples/.

4. Visit http://127.0.0.1:8000/examples/ to view the base.