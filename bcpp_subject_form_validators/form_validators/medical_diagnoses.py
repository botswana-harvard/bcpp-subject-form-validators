from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NONE

from ..constants import CANCER, HEART_DISEASE, TUBERCULOSIS, STI
from pprint import pprint


class MedicalDiagnosesFormValidator(FormValidator):

    def clean(self):
        if self.cleaned_data.get('diagnoses'):
            self.m2m_single_selection_if(NONE, m2m_field='diagnoses')
            diagnoses = []
            for diagnosis in self.cleaned_data.get('diagnoses'):
                diagnoses.append(diagnosis.short_name)
            self.required_if_true(
                HEART_DISEASE in diagnoses,
                field_required='heart_attack_record')
            self.required_if_true(
                CANCER in diagnoses,
                field_required='cancer_record')
            self.required_if_true(
                TUBERCULOSIS in diagnoses,
                field_required='tb_record')
            self.required_if_true(
                STI in diagnoses,
                field_required='sti_record')
