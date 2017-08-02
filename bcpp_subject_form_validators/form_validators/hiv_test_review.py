from django import forms
from django.conf import settings
from django.utils import timezone
from edc_base.modelform_validators import FormValidator

from ..complete_model_first import CompleteModelFirst
from ..previous_appointment_helper import PreviousAppointmentHelper


class HivTestReviewFormValidator(FormValidator):

    appointment_helper_cls = PreviousAppointmentHelper
    hiv_testing_history_model = 'bcpp_subject.hivtestinghistory'

    def clean(self):
        CompleteModelFirst(
            subject_visit=self.cleaned_data.get('subject_visit'),
            model=self.hiv_testing_history_model)
        appt_helper = self.appointment_helper_cls(**self.cleaned_data)
        hiv_test_date = self.cleaned_data.get('hiv_test_date')
        if hiv_test_date and hiv_test_date == timezone.now().date():
            raise forms.ValidationError({
                'hiv_test_date': 'Cannot be today\'s date.'})
        elif (hiv_test_date and appt_helper.previous_appointment_rdate
              and hiv_test_date <= self.appt_helper.previous_appointment_rdate.to(
                  settings.TIME_ZONE).date()):
            raise forms.ValidationError({
                'hiv_test_date':
                'Cannot be on or before last visit on {}.'.format(
                    appt_helper.previous_appointment_rdate.to(
                        settings.TIME_ZONE).date().strftime('%Y-%m-%d'))})
