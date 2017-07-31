from django import forms

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class Cd4HistoryFormValidator(FormValidator):

    def clean(self):
        if (self.cleaned_data.get('record_available') == YES
                and not self.cleaned_data.get('last_cd4_count')
                and not self.cleaned_data.get('last_cd4_drawn_date')):
            raise forms.ValidationError(
                'If last known record of CD4 count is available or known, please '
                'provide the CD4 count and the CD4 date')
        if (self.cleaned_data.get('record_available') == NO
                and (self.cleaned_data.get('last_cd4_count', None)
                     or self.cleaned_data.get('last_cd4_drawn_date', None))):
            raise forms.ValidationError(
                'If last known record of CD4 count is not available or '
                'not known, please do NOT provide the CD4 count and the '
                'CD4 date')
