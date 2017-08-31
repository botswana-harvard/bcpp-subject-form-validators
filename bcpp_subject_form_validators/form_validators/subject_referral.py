from django import forms
from edc_base.modelform_validators import FormValidator
from bcpp_referral.utils import get_required_crf


class SubjectReferralFormValidator(FormValidator):

    def clean(self):
        required_crf = get_required_crf(
            subject_visit=self.cleaned_data.get('subject_visit'))
        if required_crf:
            raise forms.ValidationError(
                'Insufficient information to prepare referral. '
                f'Complete \'{required_crf._meta.verbose_name}\' first '
                'and try again.')
