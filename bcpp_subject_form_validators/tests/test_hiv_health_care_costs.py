from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_constants.constants import NO, MALE
from edc_registration.models import RegisteredSubject

from ..form_validators import HivHealthCareCostsFormValidator
from .models import SubjectVisit


class TestHivHealthCareCostsFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    @tag('med_care')
    def test_no_med_care_none_reason_no_care(self):
        cleaned_data = dict(
            hiv_medical_care=NO, reason_no_care=None,
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    @tag('med_care')
    def test_no_med_care_with_reason_no_care(self):
        cleaned_data = dict(
            hiv_medical_care=NO, reason_no_care='I am not ready to start',
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()
