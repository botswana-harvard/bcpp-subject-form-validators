from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_constants.constants import NO, MALE, YES
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
            tobacco=YES, tobacco_current=None,
            subject_visit=self.subject_visit)
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_no_med_care_with_tobacco_current(self):
        cleaned_data = dict(
            tobacco=YES, tobacco_current=YES,
            subject_visit=self.subject_visit)
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
