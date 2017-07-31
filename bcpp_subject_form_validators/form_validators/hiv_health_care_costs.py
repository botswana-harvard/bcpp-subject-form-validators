from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class HivHealthCareCostsFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            NO,
            field='hiv_medical_care',
            field_required='reason_no_care')
        self.required_if(
            YES,
            field='hiv_medical_care',
            field_required='place_care_received')
        self.required_if(
            YES,
            field='hiv_medical_care',
            field_required='care_regularity')
        self.required_if(
            YES, field='hiv_medical_care',
            field_required='doctor_visits')
