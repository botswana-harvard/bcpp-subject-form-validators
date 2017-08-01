from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, DWTA


class UncircumcisedFormValidator(FormValidator):

    def clean(self):
        self.m2m_required_if(
            YES, field='circumcised', m2m_field='health_benefits_smc')
        self.m2m_single_selection_if(
            DWTA, m2m_field='health_benefits_smc')
        self.validate_other_specify('reason_circ')

        self.required_if(
            YES, field='service_facilities', field_required='aware_free')
