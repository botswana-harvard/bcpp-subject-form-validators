from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import MALE, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import HeartAttackFormValidator
from .models import SubjectVisit, Diagnoses


class TestHeartAttackFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_dx_heart_attack_other_required(self):
        Diagnoses.objects.all().delete()
        Diagnoses.objects.create(short_name='dx1', name='dx1')
        Diagnoses.objects.create(short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            dx_heart_attack=Diagnoses.objects.all(),
            dx_heart_attack_other=None,
            subject_visit=self.subject_visit)
        form_validator = HeartAttackFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('dx_heart_attack_other', form_validator._errors)

    def test_dx_heart_attack_other(self):
        Diagnoses.objects.all().delete()
        Diagnoses.objects.create(short_name='dx1', name='dx1')
        Diagnoses.objects.create(short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            dx_heart_attack=Diagnoses.objects.all(),
            dx_heart_attack_other='some description...',
            subject_visit=self.subject_visit)
        form_validator = HeartAttackFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('dx_heart_attack_other', form_validator._errors)
