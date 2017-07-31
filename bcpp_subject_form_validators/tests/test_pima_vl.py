from django import forms
from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from edc_base.modelform_validators import REQUIRED_ERROR
from edc_registration.models import RegisteredSubject
from edc_constants.constants import MALE, YES

from .models import SubjectVisit

from ..form_validators import PimaVlFormValidator
from edc_base.utils import get_utcnow


class TestPimaCd4FormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    @tag('24')
    def test_location(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            location=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
