from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_constants.constants import MALE, NEG, POS
from edc_registration.models import RegisteredSubject

from ..form_validators import ElisaHivResultFormValidator
from .models import SubjectVisit, HicEnrollment, SubjectRequisition
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

    def test_ok(self):
        SubjectRequisition.objects.create(
            subject_visit=self.subject_visit, panel_name='ELISA')
        ElisaHivResultFormValidator.elisa_hiv_result_model = (
            'bcpp_subject_form_validators.elisahivresult')
        ElisaHivResultFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = ElisaHivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertEqual({}, form_validator._errors)

    def test_hiv_result_datetime(self):
        SubjectRequisition.objects.create(
            subject_visit=self.subject_visit, panel_name='ELISA')
        ElisaHivResultFormValidator.elisa_hiv_result_model = (
            'bcpp_subject_form_validators.elisahivresult')
        ElisaHivResultFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hiv_result=POS)
        form_validator = ElisaHivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('hiv_result_datetime', form_validator._errors)

    def test_hiv_result_must_be_neg_if_hic_enrolled(self):
        HicEnrollment.objects.create(
            subject_visit=self.subject_visit)
        ElisaHivResultFormValidator.elisa_hiv_result_model = (
            'bcpp_subject_form_validators.elisahivresult')
        ElisaHivResultFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = ElisaHivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('hiv_result', form_validator._errors)

    def test_elisa_requisition_required(self):
        HicEnrollment.objects.create(
            subject_visit=self.subject_visit)
        ElisaHivResultFormValidator.subject_requisition_model = (
            'bcpp_subject_form_validators.subjectrequisition')
        ElisaHivResultFormValidator.hic_enrollment_model = (
            'bcpp_subject_form_validators.hicenrollment')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            hiv_result=NEG)
        form_validator = ElisaHivResultFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('hiv_result', form_validator._errors)
