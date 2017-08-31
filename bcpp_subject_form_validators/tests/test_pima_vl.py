from django import forms
from django.test import TestCase, tag
from edc_base.modelform_validators import REQUIRED_ERROR
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES
from edc_registration.models import RegisteredSubject

from .models import SubjectVisit
from ..form_validators import PimaVlFormValidator
from .reference_config_helper import ReferenceConfigHelper


class TestPimaCd4FormValidator(TestCase):

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

    def test_location(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            location=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_datetime(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            test_datetime=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_easy_of_use(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            easy_of_use=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_stability(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES,
            stability=None)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_required_fields(self):
        cleaned_data = dict(
            test_done=YES,
            location='Mmathethe',
            test_datetime=get_utcnow,
            easy_of_use=YES,
            stability=YES,
            subject_visit=self.subject_visit,)
        form_validator = PimaVlFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()
