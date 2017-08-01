from django import forms
from django.test import TestCase
from edc_constants.constants import MALE, YES, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import HivLinkageToCareFormValidator
from .models import SubjectVisit, HivCareAdherence
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
        HivLinkageToCareFormValidator.hiv_care_adherence_model = (
            'bcpp_subject_form_validators.hivcareadherence')
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit)

    def test_requires_hiv_care_adherence(self):
        HivCareAdherence.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivLinkageToCareFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivLinkageToCareFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_some_kept_appt_options_require_different_clinic(self):
        for response in ['attended_different_clinic', 'went_different_clinic']:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    kept_appt=response,
                    different_clinic=None)
                form_validator = HivLinkageToCareFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('different_clinic', form_validator._errors)

    def test_some_kept_appt_options_require_failed_attempt_date(self):
        for response in ['failed_attempt']:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    kept_appt=response,
                    failed_attempt_date=None)
                form_validator = HivLinkageToCareFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('failed_attempt_date', form_validator._errors)

    def test_evidence_referral_other(self):
        for field in ['evidence_referral', 'reason_recommended_art', 'evidence_art']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    **{field: OTHER})
                form_validator = HivLinkageToCareFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(f'{field}_other',
                              form_validator._errors)

    def test_recommended_art_reason(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            recommended_art=YES,
            reason_recommended_art=None)
        form_validator = HivLinkageToCareFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('reason_recommended_art', form_validator._errors)

    def test_initiated(self):
        for field in ['initiated_date', 'initiated_clinic',
                      'initiated_clinic_community', 'evidence_art']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    initiated=YES,
                    initiated_date='something',
                    initiated_clinic='something',
                    initiated_clinic_community='something',
                    evidence_art='something')
                cleaned_data.update({field: None})
                form_validator = HivLinkageToCareFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(field, form_validator._errors)
