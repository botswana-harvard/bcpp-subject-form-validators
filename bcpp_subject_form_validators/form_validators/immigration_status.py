from edc_base.modelform_validators import FormValidator


class ImmigrationStatusFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify('country_of_origin')
