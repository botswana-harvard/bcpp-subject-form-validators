from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.modelform_validators import NOT_REQUIRED_ERROR
from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import MALE, FEMALE
from edc_registration.models import RegisteredSubject

from ..constants import MARRIED
from ..form_validators import DemographicsFormValidator
from .models import SubjectVisit
from .reference_config_helper import ReferenceConfigHelper


class TestValidators(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        self.reference_config_helper.reconfigure(
            'bcpp_subject_form_validators')
        self.subject_identifier_male = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_male,
            gender=MALE)
        self.subject_visit_male = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_male)

        self.subject_identifier_female = '23456'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_female,
            gender=FEMALE)
        self.subject_visit_female = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_female)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_male)
        form_validator = DemographicsFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_married_female_wives_in_wrong_field(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_female,
            marital_status=MARRIED,
            husband_wives=1)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('husband_wives', form_validator._errors)

    def test_married_male_wives_in_wrong_field(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_male,
            marital_status=MARRIED,
            num_wives=1)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('num_wives', form_validator._errors)

    def test_married_female_with_no_wives(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_female,
            marital_status=MARRIED,
            num_wives=0)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('num_wives', form_validator._errors)

    def test_married_male_with_no_wives(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_male,
            marital_status=MARRIED,
            husband_wives=0)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('husband_wives', form_validator._errors)

    def test_married_male_wives(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_male,
            marital_status=MARRIED,
            husband_wives=-1)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('husband_wives', form_validator._errors)

    def test_married_female_wives(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit_female,
            marital_status=MARRIED,
            num_wives=-1)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('num_wives', form_validator._errors)
