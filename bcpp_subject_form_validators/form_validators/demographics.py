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

            self.required_if_true(
                gender == MALE, field_required='husband_wives')
            self.required_if_true(
                gender == FEMALE, field_required='num_wives')

            if gender == MALE and self.cleaned_data.get('husband_wives', 0) < 0:
                raise forms.ValidationError({
                    'husband_wives': 'Must be greater than 0'})

            if gender == FEMALE and self.cleaned_data.get('num_wives', 0) < 0:
                raise forms.ValidationError({
                    'num_wives': 'Must be greater than 0'})
        else:
            if self.cleaned_data.get('num_wives'):
                raise forms.ValidationError({
                    'num_wives': 'This field is not required'})
            if self.cleaned_data.get('husband_wives'):
                raise forms.ValidationError({
                    'husband_wives': 'This field is not required'})
