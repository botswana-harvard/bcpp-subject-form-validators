from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES

from .mobile_test_validator import MobileTestValidator


class PimaVlFormValidator(FormValidator):

    modile_test_validator_cls = MobileTestValidator

    def clean(self):
        self.applicable_if(YES, field='test_done', field_applicable='location')
        self.required_if(
            YES, field='test_done', field_required='test_datetime')
        self.required_if(YES, field='test_done', field_required='easy_of_use')
        self.required_if(YES, field='test_done', field_required='stability')
        modile_test_validator = self.modile_test_validator_cls(
            cleaned_data=self.cleaned_data)
        modile_test_validator.validate()
