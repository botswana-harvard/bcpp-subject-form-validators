from django import forms
from django.apps import apps as django_apps

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import MALE, FEMALE, DWTA

from ..constants import MARRIED, ALONE


class DemographicsFormValidator(FormValidator):

    def clean(self):
        self.registered_subject_model_cls = django_apps.get_model(
            'edc_registration.registeredsubject')
        self.validate_marriage()
        self.m2m_single_selection_if(ALONE, DWTA, m2m_field='live_with')
        self.validate_other_specify('religion', 'religion_other')
        self.validate_other_specify('ethnic', 'ethnic_other')

    def validate_marriage(self):
        # validating if married
        if self.cleaned_data.get('marital_status') == MARRIED:
            subject_visit = self.cleaned_data.get('subject_visit')
            gender = self.registered_subject_model_cls.objects.get(
                subject_identifier=subject_visit.subject_identifier).gender
            if gender == FEMALE and self.cleaned_data.get('husband_wives') is not None:
                raise forms.ValidationError(
                    {'husband_wives':
                     'This field is not required for female'})
            elif gender == MALE and self.cleaned_data.get('num_wives') is not None:
                raise forms.ValidationError(
                    {'num_wives':
                     'This field is not required for male'})
            elif self.cleaned_data.get('num_wives') is None and gender == FEMALE:
                raise forms.ValidationError(
                    {'num_wives':
                     'Expected a number greater than 0.'})
            elif self.cleaned_data.get('husband_wives') is None and gender == MALE:
                raise forms.ValidationError(
                    {'husband_wives':
                     'Expected a number greater than 0.'})
            elif gender == FEMALE and self.cleaned_data.get('num_wives') <= 0:
                raise forms.ValidationError(
                    {'num_wives':
                     'Expected a number greater than 0.'})
            elif gender == MALE and self.cleaned_data.get('husband_wives') <= 0:
                raise forms.ValidationError(
                    {'husband_wives':
                     'Expected a number greater than 0.'})
        elif self.cleaned_data.get('marital_status') != MARRIED:
            if self.cleaned_data.get('num_wives') is not None:
                raise forms.ValidationError({
                    'num_wives':
                    'This field is not required'})
            elif self.cleaned_data.get('husband_wives') is not None:
                raise forms.ValidationError({
                    'husband_wives':
                    'This field is not required'})
