from edc_base.modelform_validators import FormValidator


class TuberculosisFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify('tb_dx')
