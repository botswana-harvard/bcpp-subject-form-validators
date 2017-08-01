from django import forms
from edc_base.modelform_validators import FormValidator

from .mobile_test_validator import MobileTestValidator


class PimaCd4FormValidator(FormValidator):

    modile_test_validator_cls = MobileTestValidator

    def clean(self):
        if (self.cleaned_data.get('result_value')
                and self.cleaned_data.get('result_value') > 3000):
            forms.ValidationError({
                'result_value': 'Invalid result value.'})
        modile_test_validator = self.modile_test_validator_cls(
            cleaned_data=self.cleaned_data)
        modile_test_validator.validate()
