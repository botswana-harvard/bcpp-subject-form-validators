from edc_base.modelform_validators import FormValidator
from edc_constants.constants import DWTA, OTHER


class AccessToCareFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify('access_care')
        self.m2m_single_selection_if(
            DWTA, m2m_field='medical_care_access')
        self.m2m_other_specify(
            OTHER, m2m_field='medical_care_access',
            field_other='medical_care_access_other')
