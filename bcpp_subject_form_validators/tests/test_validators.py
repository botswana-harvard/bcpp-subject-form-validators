from django.test import TestCase, tag

from edc_constants.constants import NOT_APPLICABLE, MALE
from edc_registration.models import RegisteredSubject

from ..constants import MARRIED
from ..form_validators import AccessToCareFormValidator, CancerFormValidator
from ..form_validators import Cd4HistoryFormValidator, CeaEnrollmentChecklistFormValidator
from ..form_validators import CircumcisedFormValidator, CircumcisionFormValidator
from ..form_validators import CommunityEngagementFormValidator, DemographicsFormValidator
from ..form_validators import EducationFormValidator, HeartAttackFormValidator
from .models import SubjectVisit


class TestValidators(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_access_to_care(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = AccessToCareFormValidator(cleaned_data=cleaned_data)
        form_validator.validate()

    def test_cancer(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = CancerFormValidator(cleaned_data=cleaned_data)
        form_validator.validate()

    def test_cd4_history(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = Cd4HistoryFormValidator(cleaned_data=cleaned_data)
        form_validator.validate()

    def test_cea_enrollment_checklist(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = CeaEnrollmentChecklistFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_circumcised(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = CircumcisedFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_circumcision(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            circumcised_location=NOT_APPLICABLE)
        form_validator = CircumcisionFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_community_engagement(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_demographics(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    @tag('demographics')
    def test_demographics_married(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            marital_status=MARRIED,
            husband_wives=1)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    @tag('demographics')
    def test_demographics_married2(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            marital_status=MARRIED,
            husband_wives=None)
        form_validator = DemographicsFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_education(self):
        EducationFormValidator.subject_locator_model = (
            'bcpp_subject_form_validators.subjectlocator')
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = EducationFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_heart_attack(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit)
        form_validator = HeartAttackFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()
