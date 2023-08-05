[![Downloads](https://pepy.tech/badge/django-fast-migrations)](https://pepy.tech/project/django-fast-migrations)

# Django-Fast-Migrations

Command to speed up the application of migrations in a Django project.


## Installation

Install using pip:

```
pip install django-fast-migrations
```

Then add ``'django_fast_migrations'`` to your ``INSTALLED_APPS``.

```
INSTALLED_APPS = [
    ...
    'django_fast_migrations',
]
```

## Usage

How to execute command:

    ./manage.py migrate_by_app
    
The previous command only checks if there are applications with pending migrations.

To execute the pending migrations we have to call the command:

    ./manage.py migrate_by_app

When executed without parameters it **only checks** if there are applications with pending migrations

Possible arguments:

* ```--execute```: If pending migrations are found then execute them.
* ```--database```: Nominates a database to synchronize. Defaults to the "default" database.

