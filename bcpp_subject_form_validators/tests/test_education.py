from django import forms
from django.test import TestCase
from edc_base.modelform_validators.base_form_validator import REQUIRED_ERROR,\
    NOT_REQUIRED_ERROR
from edc_constants.constants import MALE, YES, NO
from edc_registration.models import RegisteredSubject

from ..form_validators import EducationFormValidator
from .models import SubjectVisit, SubjectLocator
from .reference_config_helper import ReferenceConfigHelper


class TestValidators(TestCase):

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
        EducationFormValidator.subject_locator_model = 'bcpp_subject_form_validators.subjectlocator'
        self.subject_locator = SubjectLocator.objects.create(
            subject_identifier=self.subject_identifier,
            may_call_work=YES)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_ok_no_locator(self):
        SubjectLocator.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_working_on_locator(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            working=NO)
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('working', form_validator._errors)

    def test_employed_monthly_income(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            working=YES,
            job_type='self full-time',
            job_description='teacher')
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('monthly_income', form_validator._errors)

    def test_employed_monthly_income_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            working=YES,
            job_type='self full-time',
            job_description='teacher',
            monthly_income='More than 10,000 pula')
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)
