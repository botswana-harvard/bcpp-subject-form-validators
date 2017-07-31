from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_registration.models import RegisteredSubject
from edc_constants.constants import NOT_APPLICABLE, MALE, YES, NO
 
from ..form_validators import UncircumcisedFormValidator
from .models import SubjectVisit
 
class TestUncircumcisedFormValidator(TestCase):
 
    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
        
    def test_done_right_facility(self):
        cleaned_data = dict(
            service_facilities=YES, aware_free='yes',
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()
        
    def test_not_done_right_facility(self):
        cleaned_data = dict(
            service_facilities=NO, aware_free=None,
            subject_visit=self.subject_visit)
        form_validator = UncircumcisedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.clean)
