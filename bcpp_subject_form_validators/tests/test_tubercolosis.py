from django.test import TestCase

from edc_constants.constants import MALE, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import TuberculosisFormValidator
from .models import SubjectVisit
from django.core.exceptions import ValidationError


class TestValidators(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = TuberculosisFormValidator(cleaned_data=cleaned_data)
        form_validator.validate()

    def test_other(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            tb_dx=OTHER)
        form_validator = TuberculosisFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('tb_dx_other', form_validator._errors)
