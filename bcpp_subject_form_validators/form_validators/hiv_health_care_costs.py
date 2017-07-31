from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class HivHealthCareCostsFormValidator(FormValidator):

    def clean(self):
        self.applicable_if(
            NO, field='hiv_medical_care', field_applicable='reason_no_care')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='place_care_received')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='care_regularity')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='doctor_visits')
