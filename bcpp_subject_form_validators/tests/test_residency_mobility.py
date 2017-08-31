from django import forms
from django.test import TestCase, tag
from edc_constants.constants import MALE, YES, NO
from edc_registration.models import RegisteredSubject

from ..constants import ZERO
from ..form_validators import ResidencyMobilityFormValidator
from .models import SubjectVisit, HicEnrollment
from .reference_config_helper import ReferenceConfigHelper


class TestFormValidator(TestCase):

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
        ResidencyMobilityFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        HicEnrollment.objects.create(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            intend_residency=NO)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            intend_residency=NO)
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_differs_with_hic_enrollment(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=NO,
            intend_residency=YES)
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)

    def test_no_hicenrollment(self):
        HicEnrollment.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            intend_residency=NO)
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_nights_away(self):
        HicEnrollment.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            nights_away='more than 6 months')
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('nights_away', form_validator._errors)

    def test_nights_away2(self):
        HicEnrollment.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            nights_away=ZERO,
            cattle_postlands=YES)
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('cattle_postlands', form_validator._errors)

    def test_cattle_postlands_other(self):
        HicEnrollment.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            permanent_resident=YES,
            nights_away=YES,
            cattle_postlands='Other community')
        form_validator = ResidencyMobilityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('cattle_postlands_other', form_validator._errors)
