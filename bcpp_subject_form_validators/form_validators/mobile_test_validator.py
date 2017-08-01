from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class MobileTestValidator(FormValidator):

    def clean(self):
        self.required_if(
            NO, field='test_done', field_required='reason_not_done')
        self.validate_other_specify('reason_not_done')
        self.required_if(
            YES, field='test_done', field_required='machine_identifier')
        self.required_if(YES, field='test_done', field_required='result_value')
        self.required_if(
            YES, field='test_done', field_required='result_datetime')
