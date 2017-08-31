from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class ReproductiveHealthFormValidator(FormValidator):

    def clean(self):
        self.not_required_if(
            YES, field='menopause', field_required='family_planning')
        self.not_required_if(
            YES, field='menopause', field_required='currently_pregnant')
        self.required_if(
            NO,
            field='menopause',
            field_required='currently_pregnant'
        )

        self.validate_other_specify(field='family_planning')

        self.required_if(
            YES,
            field='when_pregnant',
            field_required='gestational_weeks')

        self.applicable_if(
            YES, field='when_pregnant', field_applicable='pregnancy_hiv_tested')
        self.applicable_if(
            YES, field='when_pregnant', field_applicable='pregnancy_hiv_retested')
