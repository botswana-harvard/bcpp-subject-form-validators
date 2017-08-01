from django import forms
from django.test import TestCase, tag
from edc_constants.constants import MALE, NONE, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import HivRelatedIllnessFormValidator
from .models import SubjectVisit, ListModel
from .reference_config_helper import ReferenceConfigHelper


class TestValidators(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        self.reference_config_helper.reconfigure(
            'bcpp_subject_form_validators')
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
        ListModel.objects.create(name='sti1', short_name='sti1')

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            sti_dx=ListModel.objects.all())
        form_validator = HivRelatedIllnessFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_m2m_invalid_combination(self):
        ListModel.objects.create(name=NONE, short_name=NONE)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            sti_dx=ListModel.objects.all())
        form_validator = HivRelatedIllnessFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('sti_dx', form_validator._errors)

    def test_m2m_other(self):
        ListModel.objects.create(name=OTHER, short_name=OTHER)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            sti_dx=ListModel.objects.all())
        form_validator = HivRelatedIllnessFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('sti_dx_other', form_validator._errors)

    def test_m2m_options(self):
        for option in ['wasting', 'diarrhoea', 'yeast_infection', 'pneumonia', 'PCP', 'herpes']:
            with self.subTest(option=option):
                field = option.lower()
                ListModel.objects.all().delete()
                ListModel.objects.create(name=option, short_name=option)
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    sti_dx=ListModel.objects.all(),
                    **{f'{field}_date': None})
                form_validator = HivRelatedIllnessFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(f'{field}_date', form_validator._errors)
