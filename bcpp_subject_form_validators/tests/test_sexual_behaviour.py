from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import (
    NOT_REQUIRED_ERROR,
    REQUIRED_ERROR)
from edc_registration.models import RegisteredSubject
from edc_constants.constants import MALE, NO, YES

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

    def test_ever_sex_no_lifetime_sex_partners(self):
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

    def test_ever_sex_no_last_year_partners(self):
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

    def test_ever_sex_no_first_sex(self):
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

    def test_ever_sex_yes_first_sex_partner_age(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=YES,
            first_sex_partner_age=None)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_condom(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            condom=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_alcohol_sex(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            alcohol_sex=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)
