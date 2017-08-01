from django import forms
from django.apps import apps as django_apps


class CompleteModelFirst:

    def __init__(self, subject_visit=None, model=None):

        model_cls = django_apps.get_model(model)
        try:
            model_cls.objects.get(subject_visit=subject_visit)
        except model_cls.DoesNotExist:
            raise forms.ValidationError(
                f'Please complete {model_cls._meta.verbose_name} first.')
