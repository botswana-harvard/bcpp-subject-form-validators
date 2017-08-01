from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES


class CircumcisionFormValidator(FormValidator):

    def clean(self):
        self.applicable_if(YES, field='circumcised',
                           field_applicable='circumcised_location')
        self.validate_other_specify('circumcised_location')
