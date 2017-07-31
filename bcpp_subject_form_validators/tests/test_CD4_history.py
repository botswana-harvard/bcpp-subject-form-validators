from django import forms
from django.test import TestCase

from edc_base.modelform_validators import NOT_REQUIRED_ERROR
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES, NO
from edc_registration.models import RegisteredSubject

from ..form_validators import Cd4HistoryFormValidator
from .models import SubjectVisit, ListModel


class TestCd4HistoryFormValidator(TestCase):
    
    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)
  
    def test_if_cd4_count_record_available(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            record_available=YES, last_cd4_count=50,
            last_cd4_drawn_date=get_utcnow())
        form_validator = Cd4HistoryFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate() 
