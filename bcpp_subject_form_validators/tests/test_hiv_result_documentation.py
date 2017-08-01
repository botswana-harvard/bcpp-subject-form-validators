from django import forms
from django.test import TestCase, tag

from edc_constants.constants import MALE, POS, NEG, DECLINED, IND,\
    NOT_APPLICABLE
from edc_registration.models import RegisteredSubject

from ..form_validators import HivResultDocumentationFormValidator
from .models import SubjectVisit, SubjectRequisition, HicEnrollment
from bcpp_subject_form_validators.constants import NOT_PERFORMED
from edc_base.utils import get_utcnow
from bcpp_subject_form_validators.tests.models import HivTestingHistory


class TestValidators(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
        HivResultDocumentationFormValidator.hiv_testing_history_model = (
            'bcpp_subject_form_validators.hivtestinghistory')
        HivTestingHistory.objects.create(subject_visit=self.subject_visit)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivResultDocumentationFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_requires_hiv_testing_history(self):
        HivTestingHistory.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivResultDocumentationFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)
