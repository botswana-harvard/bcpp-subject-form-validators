from django import forms

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NOT_APPLICABLE


class CircumcisionFormValidator(FormValidator):

    def clean(self):
        if (self.cleaned_data.get('circumcised') == YES
                and self.cleaned_data.get('circumcised_location') == NOT_APPLICABLE):
            raise forms.ValidationError({
                'circumcised_location':
                'This field is applicable'})
        elif (self.cleaned_data.get('circumcised') != YES
              and self.cleaned_data.get('circumcised_location') != NOT_APPLICABLE):
            raise forms.ValidationError({
                'circumcised_location':
                'This field is not applicable'})
        self.validate_other_specify('circumcised_location')
