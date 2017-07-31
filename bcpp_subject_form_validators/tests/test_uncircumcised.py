from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import NOT_APPLICABLE, MALE, YES, NO
from edc_registration.models import RegisteredSubject

from ..form_validators import UncircumcisedFormValidator
from .models import SubjectVisit
from ..tests.models import CircumcisionBenefits


@tag('UncircumcisedForm')
class TestUncircumcisedFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    @tag('facility')
    def test_done_right_facility(self):
        cleaned_data = dict(
            service_facilities=YES, aware_free=YES,
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    @tag('facility')
    def test_not_done_right_facility(self):
        cleaned_data = dict(
            service_facilities=YES, aware_free=None,
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('aware_free', form_validator._errors)

    @tag('circumcized')
    def test_circumcised(self):
        CircumcisionBenefits.objects.create(
            name='reduce_hiv_infection')
        cleaned_data = dict(
            circumcised=YES,
            health_benefits_smc=CircumcisionBenefits.objects.all(),
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    @tag('circumcized')
    def test_circumcised_1(self):
        cleaned_data = dict(
            circumcised=YES,
            health_benefits_smc=[],
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('health_benefits_smc', form_validator._errors)
