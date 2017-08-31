from django import forms
from django.test import TestCase, tag
from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import MALE, YES, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import HypertensionCardiovascularFormValidator
from .models import SubjectVisit, ListModel
from .reference_config_helper import ReferenceConfigHelper


class TestHypertensionCardiovascularFormValidator(TestCase):

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

    def test_no_med_care_none_tobacco_current(self):
        cleaned_data = dict(
            tobacco=YES, tobacco_current=None, tobacco_counselling=YES,
            subject_visit=self.subject_visit)
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('tobacco_current', form_validator._errors)

    def test_yes_hypertension_diagnosis_with_medication_taken(self):
        for medication_taken in [None, ListModel.objects.all()]:
            with self.subTest(medication_taken=medication_taken):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    hypertension_diagnosis=YES,
                    health_care_facility='government clinic',
                    medication_taken=medication_taken
                )
                form_validator = HypertensionCardiovascularFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('medication_taken', form_validator._errors)

    def test_yes_hypertension_diagnosis_with_medication_given(self):
        for medication_given in [None, ListModel.objects.all()]:
            with self.subTest(medication_given=medication_given):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    hypertension_diagnosis=YES,
                    health_care_facility='government clinic',
                    medication_given=medication_given
                )
                form_validator = HypertensionCardiovascularFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('medication_taken', form_validator._errors)

    def test_medication_taken_other_require_medication_taken_other(self):
        ListModel.objects.create(
            short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hypertension_diagnosis=YES,
            health_care_facility='government clinic',
            medication_taken=ListModel.objects.all())
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('medication_taken_other', form_validator._errors)

    def test_medication_given_other_require_medication_given_other(self):
        ListModel.objects.create(
            short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hypertension_diagnosis=YES,
            health_care_facility='government clinic',
            medication_given=ListModel.objects.all(),
            medication_taken=ListModel.objects.all())
        form_validator = HypertensionCardiovascularFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('medication_taken_other', form_validator._errors)
