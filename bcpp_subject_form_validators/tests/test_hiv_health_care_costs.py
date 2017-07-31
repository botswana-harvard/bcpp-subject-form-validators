from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_constants.constants import NO, MALE, YES
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

    def test_no_med_care_none_reason_no_care(self):
        cleaned_data = dict(
            hiv_medical_care=NO, reason_no_care=None,
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_no_med_care_with_reason_no_care(self):
        cleaned_data = dict(
            hiv_medical_care=NO, reason_no_care='I am not ready to start',
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_yes_med_care_none_reason_no_care(self):
        cleaned_data = dict(
            hiv_medical_care=YES, reason_no_care=None,
            place_care_received='Government dispensary',
            care_regularity='Government dispensary',
            doctor_visits='1 time',
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_yes_med_care_with_none_place_care_received(self):
        cleaned_data = dict(
            hiv_medical_care=YES, place_care_received=None,
            care_regularity=None,
            doctor_visits=None,
            subject_visit=self.subject_visit)
        form_validator = HivHealthCareCostsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
