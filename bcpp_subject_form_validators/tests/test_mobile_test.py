from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
 
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES, NO
from edc_registration.models import RegisteredSubject
 
from ..form_validators import MobileTestValidator
from .models import SubjectVisit
 
 
class TestMobileTestValidator(TestCase):
     
    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
         
    def test_reason_test_not_done(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=NO, reason_not_done=None)
        form_validator = MobileTestValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('reason_not_done', form_validator._errors) 
    
    def test_machine_identifier_required(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES, machine_identifier=None)
        form_validator = MobileTestValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('machine_identifier', form_validator._errors)  
         
    def test_result_value_no_specified(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES, result_value=None,
            machine_identifier='w345')
        form_validator = MobileTestValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('result_value', form_validator._errors)   
         
    def test_result_datetime_no_specified(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            test_done=YES, result_datetime=None,
            machine_identifier='w345', result_value=50)
        form_validator = MobileTestValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            pass
        self.assertIn('result_datetime', form_validator._errors)
