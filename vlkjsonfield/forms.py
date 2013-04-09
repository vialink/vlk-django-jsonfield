# coding: utf-8

from django.forms.models import ModelForm


class JSONModelForm(ModelForm):
    """ It supports using fields from model field type VLKJSONField.

    XXX What should we do if JSONField field of model doesn't have "subfields"?
        For example: extra__address or extra__address__street? Should we create it?

    Example
    -------
    class MyModel(models.Model):
        extra = JSONField()

    class MyForm(JSONModelForm):
        extra__name = forms.CharField()
        extra__age = forms.IntegerField()
        extra__email = forms.MailField()
        extra__is_male = forms.BooleanField()
    """
    SEPARATOR = '__'

    def get_or_set_jsonfields(self, instance, formfield_name):
        keys = formfield_name.split(self.SEPARATOR)
        modelfield_name = keys[0]
        fieldnode_name = keys[-1]
        obj = getattr(instance, modelfield_name)
        for i in range(1, len(keys) - 1):
            obj = obj[keys[i]]
        return obj, fieldnode_name

    def is_jsonfield(self, formfield_name):
        """ Check if `formfield_name` is a JSONField in model.

        TODO Verify if model has a JSONField with this name.
        """
        if self.SEPARATOR in formfield_name:
            return True
        return False

    def get_jsonfield(self, formfield_name):
        """ Get a value from `self.instance` field `formfield_name`.
        """
        obj, fieldnode_name = self.get_or_set_jsonfields(self.instance, formfield_name)
        return obj[fieldnode_name]

    def __init__(self, *args, **kwargs):
        """ Loads the instance JSONField fields data into form.

        Following django policies, it is done only if it wouldn't override
        initial value.
        """
        super(JSONModelForm, self).__init__(*args, **kwargs)

        # Adding JSONField values from instance to form initial
        for k, v in self.fields.items():
            if self.is_jsonfield(k) and k not in self.initial:
                self.initial[k] = self.get_jsonfield(k)

    def save(self, commit):
        """ Saves the form `cleaned_data` data of JSONField fields in instance.
        """
        instance = super(JSONModelForm, self).save(commit=False)

        # Adding cleaned_data values to JSONFields instances
        for k, v in self.fields.items():
            if self.is_jsonfield(k):
                obj, fieldnode_name = self.get_or_set_jsonfields(instance, k)
                obj[fieldnode_name] = self.cleaned_data[k]

        if commit:
            instance.save()

        return instance
