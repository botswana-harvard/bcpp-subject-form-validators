from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES


class PimaVlFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='test_done',
            field_required='location')

        self.required_if(
            YES,
            field='test_done',
            field_required='test_datetime')

        self.required_if(
            YES,
            field='test_done',
            field_required='easy_of_use')

        self.required_if(
            YES,
            field='test_done',
            field_required='stability')
