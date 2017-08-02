from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO, DWTA

from ..previous_appointment_helper import PreviousAppointmentHelper


class SexualBehaviourFormValidator(FormValidator):

    appointment_helper_cls = PreviousAppointmentHelper
    sexual_behaviour_model = 'bcpp_subject.sexualbehaviour'

    def clean(self):
        self.not_required_if(
            NO, DWTA,
            field='ever_sex',
            field_required='lifetime_sex_partners',
            optional_if_dwta=True)

        self.not_required_if(
            NO, DWTA,
            field='ever_sex',
            field_required='last_year_partners',
            optional_if_dwta=True)

        last_year_partners = int(
            self.cleaned_data.get('last_year_partners', 0))
        lifetime_sex_partners = int(
            self.cleaned_data.get('lifetime_sex_partners', 0))
        if last_year_partners > lifetime_sex_partners:
            raise forms.ValidationError({
                'last_year_partners':
                f'May not exceed "{lifetime_sex_partners}" lifetime partners.'})

        self.required_if_true(
            last_year_partners > 0, field_required='more_sex')

        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='first_sex',
            optional_if_dwta=True)

        self.validate_first_sex_age()

        self.required_if(
            YES, DWTA,
            field='ever_sex',
            field_required='first_sex_partner_age')

        self.validate_other_specify(
            'first_sex_partner_age', other_stored_value='gte_19')

        self.not_required_if(
            NO, DWTA,
            field='ever_sex',
            field_required='condom',
            optional_if_dwta=True)

        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='alcohol_sex',
            optional_if_dwta=True)

        self.validate_ever_sex_with_previous_instance()

    def validate_first_sex_age(self):
        age_in_years = self.cleaned_data.get(
            'subject_visit').household_member.age_in_years
        if (self.cleaned_data.get('first_sex') and age_in_years
                and (int(age_in_years) < int(self.cleaned_data.get('first_sex')))):
            raise forms.ValidationError({
                'first_sex': f'Invalid. Participant is {age_in_years} years old.'})

    def validate_ever_sex_with_previous_instance(self):
        appt_helper = self.appointment_helper_cls(**self.cleaned_data)
        sexual_behaviour_model_cls = django_apps.get_model(
            self.sexual_behaviour_model)
        try:
            sexual_behaviour_model_cls.objects.get(
                subject_visit__appointment=appt_helper.previous_appointment,
                ever_sex=YES)
        except sexual_behaviour_model_cls.DoesNotExist:
            pass
        else:
            if self.cleaned_data.get('ever_sex') not in [YES, DWTA]:
                raise forms.ValidationError({
                    'ever_sex':
                    'Expected \'Yes\' as previously reported on {}. '
                    '(DWTA is also acceptable)'.format(
                        appt_helper.previous_appointment_rdate.date().strftime(
                            '%Y-%m-%d'))})
