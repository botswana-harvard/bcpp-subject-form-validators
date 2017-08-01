from django import forms
from django.test import TestCase

from edc_constants.constants import MALE, YES, NO
from edc_registration.models import RegisteredSubject

from ..form_validators import EducationFormValidator
from .models import SubjectVisit, SubjectLocator


class TestValidators(TestCase):

    def setUp(self):
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

    def test_unemployed(self):
        self.subject_locator.may_call_work = NO
        self.subject_locator.save()
        for response in ['student', 'retired']:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    working=NO,
                    reason_unemployed=response)
                form_validator = EducationFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('monthly_income', form_validator._errors)
