from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, OTHER, NO


class HypertensionCardiovascularFormValidator(FormValidator):

    def clean(self):
        self.applicable_if(
            YES, field='tobacco',
            field_applicable='tobacco_current')
        self.applicable_if(
            YES, field='tobacco',
            field_applicable='tobacco_counselling')

        self.applicable_if(
            YES, field='hypertension_diagnosis',
            field_applicable='health_care_facility')

        self.m2m_required_if(
            YES, field='hypertension_diagnosis', m2m_field='medication_taken')
        self.m2m_other_specify(
            OTHER, m2m_field='medication_taken', field_other='medication_taken_other')

        self.m2m_required_if(
            YES, field='hypertension_diagnosis', m2m_field='medication_given')
        self.m2m_other_specify(
            OTHER, m2m_field='medication_given', field_other='medication_given_other')

        self.applicable_if(
            NO, field='bp',
            field_applicable='bp_refused_reason')

        self.required_if(
            YES, field='bp', field_required='right_arm_one')
        self.required_if(
            YES, field='bp', field_required='left_arm_one')
        self.required_if(
            YES, field='bp', field_required='right_arm_two')
        self.required_if(
            YES, field='bp', field_required='left_arm_two')

        self.applicable_if(
            NO, field='bm',
            field_applicable='bm_refused_reason')

        self.required_if(
            YES, field='bm', field_required='waist_reading_one')
        self.required_if(
            YES, field='bm', field_required='waist_reading_two')
        self.required_if(
            YES, field='bm', field_required='hip_reading_one')
        self.required_if(
            YES, field='bm', field_required='hip_reading_two')
