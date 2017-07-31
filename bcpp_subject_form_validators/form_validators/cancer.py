from edc_base.modelform_validators import FormValidator


class CancerFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify('cancer_dx')
