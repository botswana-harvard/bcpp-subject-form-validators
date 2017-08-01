from bcpp_status.status_helper import StatusHelper
from bcpp_status.tests import ReferenceTestHelper, StatusHelperTestMixin
from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, NEG, NO, YES, POS, IND
from edc_registration.models import RegisteredSubject

from ..form_validators import HicEnrollmentFormValidator
from .models import SubjectLocator, ResidencyMobility, HivResult
from .models import SubjectVisit, SubjectConsent, ElisaHivResult, HivtestReview
from .reference_config_helper import ReferenceConfigHelper


class TestValidators(StatusHelperTestMixin, TestCase):

    reference_config_helper = ReferenceConfigHelper()
    reference_helper_cls = ReferenceTestHelper

    def setUp(self):
        self.subject_identifier = '12345'
        self.reference_config_helper.reconfigure(
            'bcpp_subject_form_validators')
        self.reference_helper = self.reference_helper_cls(
            visit_model='bcpp_subject_form_validators.subjectvisit',
            subject_identifier=self.subject_identifier)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
        HicEnrollmentFormValidator.subject_consent_model = (
            'bcpp_subject_form_validators.subjectconsent')
        HicEnrollmentFormValidator.subject_requisition_model = (
            'bcpp_subject_form_validators.subjectlocator')
        HicEnrollmentFormValidator.subject_locator_model = (
            'bcpp_subject_form_validators.subjectlocator')
        HicEnrollmentFormValidator.residency_mobility_model = (
            'bcpp_subject_form_validators.residencymobility')
        HicEnrollmentFormValidator.elisa_hiv_result_model = (
            'bcpp_subject_form_validators.elisahivresult')
        HicEnrollmentFormValidator.hiv_result_model = (
            'bcpp_subject_form_validators.hivresult')
        StatusHelper.visit_model = 'bcpp_subject_form_validators.subjectvisit'
        StatusHelper.app_label = 'bcpp_subject_form_validators'
        HicEnrollmentFormValidator.status_helper_cls = StatusHelper
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            citizen=YES)
        self.subject_locator = SubjectLocator.objects.create(
            subject_identifier=self.subject_identifier,
            subject_cell='12345678')
        self.residency_mobility = ResidencyMobility.objects.create(
            subject_visit=self.subject_visit,
            permanent_resident=YES)
        self.hiv_result = HivResult.objects.create(
            subject_visit=self.subject_visit,
            hiv_result=NEG)
        HivtestReview.objects.create(
            subject_visit=self.subject_visit,
            recorded_hiv_result=NEG)
        status_helper = StatusHelper(visit=self.subject_visit)
        print(status_helper.final_hiv_status)

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_requires_consent(self):
        SubjectConsent.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)
        self.assertIn('subject consent',
                      str(form_validator._errors.get('__all__')))

    def test_requires_locator(self):
        SubjectLocator.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)
        self.assertIn('subject locator',
                      str(form_validator._errors.get('__all__')))

    def test_no_hic_permission_raises(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=NO)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hic_permission', form_validator._errors)

    def test_age(self):
        dob = (get_utcnow() - relativedelta(years=1)).date()
        self.subject_consent.dob = dob
        self.subject_consent.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('invalid_age', form_validator._error_codes)

    def test_residency(self):
        self.residency_mobility.permanent_resident = NO
        self.residency_mobility.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('invalid_residency', form_validator._error_codes)

    def test_is_hiv_negative(self):
        self.hiv_result.hiv_result = POS
        self.hiv_result.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('invalid_hiv_status', form_validator._error_codes)

    def test_is_hiv_ind(self):
        self.hiv_result.hiv_result = IND
        self.hiv_result.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('missing_elisa_hiv_result', form_validator._error_codes)

    @tag('1')
    def test_citizenship(self):
        self.subject_consent.citizen = NO
        self.subject_consent.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('invalid_citizenship', form_validator._error_codes)

    def test_locator(self):
        self.subject_locator.subject_cell = None
        self.subject_locator.save()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hic_permission=YES)
        form_validator = HicEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('invalid_locator', form_validator._error_codes)
