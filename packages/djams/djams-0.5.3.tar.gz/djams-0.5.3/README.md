# django-microsite-bindings

![Develop Branch Build Status]('testing')

Bindings for django microsites


## Installation

    pip install django_microsite_bindings

Then, just add `django_analytics_microsites` to `INSTALLED_APPS` in your Django `settings.py` file and the django_microsite_bindings.middleware to  `MIDDLEWARE`

Note that this package requires version 2.0 or greater of Django, due to the use of the `path` function for registering routes.