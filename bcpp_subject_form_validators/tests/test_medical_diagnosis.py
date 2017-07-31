from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import INVALID_ERROR, REQUIRED_ERROR, NOT_REQUIRED_ERROR
from edc_constants.constants import MALE, NONE, YES
from edc_registration.models import RegisteredSubject

from ..constants import HEART_DISEASE, CANCER, TUBERCULOSIS, STI
from ..form_validators import MedicalDiagnosesFormValidator
from .models import SubjectVisit, Diagnoses


class TestValidators(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_medical_diagnosis_no_dx(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            diagnoses=None)
        form_validator = MedicalDiagnosesFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_medical_diagnosis_invalid_combination(self):
        Diagnoses.objects.create(short_name='dx1', name='dx1')
        Diagnoses.objects.create(short_name=NONE, name=NONE)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            diagnoses=Diagnoses.objects.all())
        form_validator = MedicalDiagnosesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(INVALID_ERROR, form_validator._error_codes)

    def test_medical_diagnosis_is_required(self):
        opts = dict(
            cancer_record=CANCER,
            heart_attack_record=HEART_DISEASE,
            tb_record=TUBERCULOSIS,
            sti_record=STI)
        for field, option in opts.items():
            with self.subTest(field=field, option=option):
                Diagnoses.objects.all().delete()
                Diagnoses.objects.create(short_name='dx1', name='dx1')
                Diagnoses.objects.create(short_name=option, name=option)
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    diagnoses=Diagnoses.objects.all(),
                    **{field: None})
                form_validator = MedicalDiagnosesFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
                self.assertIn(field, form_validator._errors)

    def test_medical_diagnosis_not_required(self):
        opts = dict(
            cancer_record=CANCER,
            heart_attack_record=HEART_DISEASE,
            tb_record=TUBERCULOSIS,
            sti_record=STI)
        for field, option in opts.items():
            with self.subTest(field=field, option=option):
                Diagnoses.objects.all().delete()
                Diagnoses.objects.create(short_name='dx1', name='dx1')
                Diagnoses.objects.create(short_name=option, name=option)
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    diagnoses=Diagnoses.objects.exclude(name=option),
                    **{field: YES})
                form_validator = MedicalDiagnosesFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)
                self.assertIn(field, form_validator._errors)
