from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import MALE, YES
from edc_registration.models import RegisteredSubject

from ..form_validators import HypertensionCardiovascularFormValidator
from .models import SubjectVisit


class TestHypertensionCardiovascularFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_no_med_care_none_tobacco_current(self):
        cleaned_data = dict(
            tobacco=YES, tobacco_current=None, tobacco_counselling=YES,
            subject_visit=self.subject_visit)
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('tobacco_current', form_validator._errors)

    def test_no_med_care_with_tobacco_current(self):
        cleaned_data = dict(
            tobacco=YES, tobacco_current=YES, tobacco_counselling=YES,
            subject_visit=self.subject_visit)
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
