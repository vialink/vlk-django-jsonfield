VLK JSONField
=============

A model JSONField with an integrated form for django.

Before doing this app we looked up for a JSONField implementation, but all that we have found had nothing that fit our needs. Our needs are just a model field to store a json string and a form that is able to validate user input against our json fields requirements.

Installation
------------

Just copy this project to any folder in your computer or use pip.

    pip install vlk-django-jsonfield

Usage
-----

### Model

To create your JSONField just use the same notation as an usual model field:

    jsonfield = VLKJSONField(null=True, default=lambda: {'field1': False, 'field2': 'abc'})

[You must use lambda when using a dict as default] (https://docs.djangoproject.com/en/dev/ref/models/fields/#default)

### Form

To use this field in a form just use the form field with the same name of your model field and the subname separated by `__`:

    jsonfield__field1 = forms.CharField()
    jsonfield__field2 = forms.IntegerField(required=False)

The right side is the usual of a form field.

Who is using
------------

This project is used in Vialink software since January, 2013. Are you using it? Let us know :)

Contributing
------------

Do the usual github fork and pull request dance.

Authors
-------

* 2013 [Pedro Ferreira] (https://github.com/pedroferreira1)
* 2013 [Patrícia Borges] (https://github.com/patriciaborges)
* 2013 [Marcelo Salhab Brogliato] (https://github.com/msbrogli)
* 2013 [Jan Segre] (https://github.com/jansegre)

License
-------

Released under the MIT license. Read LICENSE.md for more information.
