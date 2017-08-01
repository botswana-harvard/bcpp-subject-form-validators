from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import MALE, NO, YES, NOT_APPLICABLE
from edc_registration.models import RegisteredSubject

from ..form_validators import ReproductiveHealthFormValidator
from .models import SubjectVisit
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

    def test(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = ReproductiveHealthFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_when_pregnant_no(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            when_pregnant=NO)
        form_validator = ReproductiveHealthFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_when_pregnant_yes(self):
        for field in ['gestational_weeks', 'pregnancy_hiv_tested', 'pregnancy_hiv_retested']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    when_pregnant=YES,
                    gestational_weeks=YES,
                    pregnancy_hiv_tested=YES,
                    pregnancy_hiv_retested=YES)
                cleaned_data.update({field: NOT_APPLICABLE})
                form_validator = ReproductiveHealthFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except ValidationError:
                    pass
                self.assertIn(field, form_validator._errors)
