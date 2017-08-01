from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_constants.constants import MALE
from edc_registration.models import RegisteredSubject

from ..form_validators import ResourceUtilizationFormValidator
from .models import SubjectVisit


class TestFormValidator(TestCase):

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
        form_validator = ResourceUtilizationFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_medical_cover(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            money_spent=1000,
            medical_cover=None)
        form_validator = ResourceUtilizationFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('medical_cover', form_validator._errors)

    def test_medical_cover_not_required(self):
        for response in [None, 0]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    money_spent=response,
                    medical_cover=None)
                form_validator = ResourceUtilizationFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except ValidationError:
                    pass
                self.assertNotIn('medical_cover', form_validator._errors)
