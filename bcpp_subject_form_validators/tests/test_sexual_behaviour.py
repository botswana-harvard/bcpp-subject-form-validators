from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import NOT_REQUIRED_ERROR
from edc_registration.models import RegisteredSubject
from edc_constants.constants import MALE, NO

from .models import SubjectVisit

from ..form_validators import SexualBehaviourFormValidator
from edc_base.utils import get_utcnow


class TestSexualBehaviourFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    @tag('111')
    def test_lifetime_sex_partners_no(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            lifetime_sex_partners=1)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    @tag('111')
    def test_last_year_partners_no(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            last_year_partners=1)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    @tag('111')
    def test_first_sex_no(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            first_sex=get_utcnow)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)
