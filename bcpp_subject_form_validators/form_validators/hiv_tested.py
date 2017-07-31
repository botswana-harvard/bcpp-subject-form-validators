from edc_base.modelform_validators import FormValidator


class HivTestedFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify('where_hiv_test')
