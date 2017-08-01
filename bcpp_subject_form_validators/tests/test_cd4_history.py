from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import MALE, YES
from edc_registration.models import RegisteredSubject

from ..form_validators import Cd4HistoryFormValidator
from .models import SubjectVisit
from .reference_config_helper import ReferenceConfigHelper


class TestCd4HistoryFormValidator(TestCase):

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

    def test_if_last_cd4_count_available(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            record_available=YES, last_cd4_count=None)
        form_validator = Cd4HistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('last_cd4_count', form_validator._errors)

    def test_if_last_cd4_drawn_date_required(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            record_available=YES, last_cd4_count=45,
            last_cd4_drawn_date=None)
        form_validator = Cd4HistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('last_cd4_drawn_date', form_validator._errors)
