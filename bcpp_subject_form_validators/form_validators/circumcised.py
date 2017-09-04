from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, DWTA, NOT_SURE


class CircumcisedFormValidator(FormValidator):

    def clean(self):
        self.m2m_required_if(
            YES, field='circumcised', m2m_field='health_benefits_smc')
        self.m2m_single_selection_if(
            DWTA, NOT_SURE, m2m_field='health_benefits_smc')
        self.required_if_not_none(
            field='when_circ', field_required='age_unit_circ')
        self.validate_other_specify('reason_circ')
        self.validate_other_specify('why_circ')
