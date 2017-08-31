from django import forms
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, POS, NEG, DECLINED, IND, NOT_APPLICABLE
from edc_registration.models import RegisteredSubject

from ..constants import NOT_PERFORMED
from ..form_validators import HivResultFormValidator
from .models import SubjectVisit, SubjectRequisition, HicEnrollment
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
        HivResultFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        HivResultFormValidator.subject_requisition_model = (
            'bcpp_subject_form_validators.subjectrequisition')
        HivResultFormValidator.microtube_panel_name = 'Microtube'
        SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel_name='Microtube')

    def test_ok(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_requires_microtube_requisition(self):
        SubjectRequisition.objects.all().delete()
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HivResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('__all__', form_validator._errors)

    def test_not_requires_microtube_requisition(self):
        SubjectRequisition.objects.all().delete()
        for response in [DECLINED, NOT_PERFORMED]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    hiv_result=response)
                form_validator = HivResultFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertNotIn('__all__', form_validator._errors)

    def test_hiv_result_must_be_neg_if_hic_enrolled(self):
        HicEnrollment.objects.create(subject_visit=self.subject_visit)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hiv_result=POS)
        form_validator = HivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hiv_result', form_validator._errors)

    def test_hiv_result_must_be_neg_if_hic_enrolled2(self):
        HicEnrollment.objects.create(subject_visit=self.subject_visit)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hiv_result=NEG)
        form_validator = HivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('hiv_result', form_validator._errors)

    def test_requires_hiv_result_datetime_if_hiv_result(self):
        for response in [POS, NEG, IND]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    hiv_result=response,
                    hiv_result_datetime=None)
                form_validator = HivResultFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('hiv_result_datetime', form_validator._errors)

    def test_blood_draw_type_applicable_if_hiv_result(self):
        for response in [POS, NEG, IND]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    hiv_result=response,
                    hiv_result_datetime=get_utcnow(),
                    blood_draw_type=NOT_APPLICABLE)
                form_validator = HivResultFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('blood_draw_type', form_validator._errors)
