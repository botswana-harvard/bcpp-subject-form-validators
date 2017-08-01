from django import forms

from edc_base.modelform_validators.form_validator import FormValidator
from edc_constants.constants import YES, NO


class CeaEnrollmentChecklistFormValidator(FormValidator):

    def clean(self):
        # TODO: these are the same as from consent, messages should be the
        # same of code should be mixed in.
        # If not a citizen, are they legall married to a Botswana citizen
        if (self.cleaned_data.get('citizen') == NO
                and not self.cleaned_data.get('legal_marriage')):
            raise forms.ValidationError(
                'if participant is not a citizen, is he/she married '
                'to a Botswana Citizen?')
        # if legally married, do they have a marriage certificate
        if (self.cleaned_data.get('legal_marriage') == YES
                and not self.cleaned_data.get('marriage_certificate')):
            raise forms.ValidationError(
                'if participant is legally married to a Botswana Citizen, '
                'Where is the marriage certificate?')
        # if there is a certificate what is the marriage certificate number
        if (self.cleaned_data.get('marriage_certificate') == YES
                and not self.cleaned_data.get('marriage_certificate_no')):
            raise forms.ValidationError(
                'if participant is legally married an has a marriage '
                'certificate, What is the marriage certificate no?')
