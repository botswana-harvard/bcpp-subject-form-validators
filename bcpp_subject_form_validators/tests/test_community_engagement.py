from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import REQUIRED_ERROR
from edc_constants.constants import MALE, OTHER
from edc_registration.models import RegisteredSubject

from ..form_validators import CommunityEngagementFormValidator
from .models import SubjectVisit, ListModel


class TestHeartAttackFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_problems_engagement_other_required(self):
        ListModel.objects.all().delete()
        ListModel.objects.create(short_name='dx1', name='dx1')
        ListModel.objects.create(short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            problems_engagement=ListModel.objects.all(),
            problems_engagement_other=None,
            subject_visit=self.subject_visit)
        form_validator = CommunityEngagementFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
        self.assertIn('problems_engagement_other', form_validator._errors)

#     @tag('eng')
#     def test_dx_heart_attack_other(self):
#         ListModel.objects.all().delete()
#         ListModel.objects.create(short_name='dx1', name='dx1')
#         ListModel.objects.create(short_name=OTHER, name=OTHER)
#         cleaned_data = dict(
#             problems_engagement=ListModel.objects.all(),
#             problems_engagement_other='some description...',
#             subject_visit=self.subject_visit)
#         form_validator = CommunityEngagementFormValidator(
#             cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except forms.ValidationError:
#             pass
#         self.assertNotIn('problems_engagement_other', form_validator._errors)
