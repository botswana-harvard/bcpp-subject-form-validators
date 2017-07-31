from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_constants.constants import YES, NO
from edc_registration.models import RegisteredSubject

from ..form_validators import HeartAttackFormValidator
from .models import SubjectVisit


class TestHeartAttackFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    @tag('heart')
    def test_dx_heart_attack(self):
        cleaned_data = dict(
            heart_attack=YES, reason_no_care=None,
            subject_visit=self.subject_visit)
        form_validator = HeartAttackFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    @tag('heart')
    def test_dx_no_heart_attack(self):
        cleaned_data = dict(
            heart_attack=NO, reason_no_care='heart disease',
            subject_visit=self.subject_visit)
        form_validator = HeartAttackFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
