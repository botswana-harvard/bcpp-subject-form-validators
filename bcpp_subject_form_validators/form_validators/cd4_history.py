from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES


class Cd4HistoryFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES, field='record_available', field_required='last_cd4_count')
        self.required_if(
            YES, field='record_available', field_required='last_cd4_drawn_date')
