from django import forms
from django.apps import apps as django_apps


class CompleteModelFirst:

    def __init__(self, subject_visit=None, subject_identifier=None, model=None):

        self.model_obj = None
        model_cls = django_apps.get_model(model)
        if subject_visit:
            opts = dict(subject_visit=subject_visit)
        else:
            opts = dict(subject_identifier=subject_identifier)
        try:
            self.model_obj = model_cls.objects.get(**opts)
        except model_cls.DoesNotExist:
            raise forms.ValidationError(
                f'Please complete {model_cls._meta.verbose_name} first.')
