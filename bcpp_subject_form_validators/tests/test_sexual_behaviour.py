from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.modelform_validators import NOT_REQUIRED_ERROR, REQUIRED_ERROR
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, NO, YES, NOT_APPLICABLE
from edc_registration.models import RegisteredSubject

from ..form_validators import SexualBehaviourFormValidator
from .models import SubjectVisit, HouseholdMember, SexualBehaviour
from .reference_config_helper import ReferenceConfigHelper


class TestSexualBehaviourFormValidator(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        self.reference_config_helper.reconfigure(
            'bcpp_subject_form_validators')
        self.subject_identifier = '12345'
        household_member = HouseholdMember.objects.create(
            subject_identifier=self.subject_identifier,
            age_in_years=25)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        for index, dte in enumerate([get_utcnow() - relativedelta(years=1), get_utcnow()]):
            appointment = Appointment.objects.create(
                subject_identifier=self.subject_identifier,
                appt_datetime=dte,
                timepoint_datetime=dte,
                visit_code=f'T{index}')
            self.subject_visit = SubjectVisit.objects.create(
                appointment=appointment,
                subject_identifier=self.subject_identifier,
                household_member=household_member)

    def test_ever_sex_no_lifetime_sex_partners(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            lifetime_sex_partners=1)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_last_year_partners(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            last_year_partners=1)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_first_sex(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            first_sex=get_utcnow)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_yes_first_sex_partner_age(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=YES,
            first_sex_partner_age=None)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_condom(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            condom=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_ever_sex_no_alcohol_sex(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            alcohol_sex=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_first_sex_age_invalid(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            first_sex=26)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('first_sex', form_validator._errors)

    def test_last_year_partners_gt_0_means_more_sex_is_required(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            lifetime_sex_partners=1,
            last_year_partners=1,
            more_sex=NOT_APPLICABLE)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('more_sex', form_validator._errors)

    def test_last_year_partners_eq_0_means_more_sex_is_not_required(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            lifetime_sex_partners=0,
            last_year_partners=0,
            more_sex=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('more_sex', form_validator._errors)

    def test_last_year_partners_exceeds_lifetime(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            lifetime_sex_partners=0,
            last_year_partners=1)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('last_year_partners', form_validator._errors)

    def test_ever_sex(self):
        SexualBehaviourFormValidator.sexual_behaviour_model = (
            'bcpp_subject_form_validators.sexualbehaviour')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            first_sex_partner_age=16,
            ever_sex=YES)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('ever_sex', form_validator._errors)

    def test_ever_sex_does_not_match_previous_yes(self):
        subject_visits = SubjectVisit.objects.all().order_by('report_datetime')
        SexualBehaviour.objects.create(
            subject_visit=subject_visits[0],
            ever_sex=YES)
        SexualBehaviourFormValidator.sexual_behaviour_model = (
            'bcpp_subject_form_validators.sexualbehaviour')
        cleaned_data = dict(
            subject_visit=subject_visits[1],
            ever_sex=NO)
        form_validator = SexualBehaviourFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('ever_sex', form_validator._errors)
