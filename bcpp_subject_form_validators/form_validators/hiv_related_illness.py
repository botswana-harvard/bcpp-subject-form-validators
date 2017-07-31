from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NONE, OTHER


class HivRelatedIllnessFormValidator(FormValidator):

    def clean(self):
        self.m2m_single_selection_if(NONE, m2m_field='sti_dx')
        self.m2m_other_specify(
            OTHER, m2m_field='sti_dx', field_other='sti_dx_other')
        diagnoses = []
        for diagnosis in self.cleaned_data.get('sti_dx'):
            diagnoses.append(diagnosis.short_name)
        self.required_if_true(
            'wasting' in diagnoses,
            field_required='wasting_date')
        self.required_if_true(
            'diarrhoea' in diagnoses,
            field_required='diarrhoea_date')
        self.required_if_true(
            'yeast_infection' in diagnoses,
            field_required='yeast_infection_date')
        self.required_if_true(
            'pneumonia' in diagnoses,
            field_required='pneumonia_date')
        self.required_if_true(
            'PCP' in diagnoses,
            field_required='pcp_date')
        self.required_if_true(
            'herpes' in diagnoses,
            field_required='herpes_date')
