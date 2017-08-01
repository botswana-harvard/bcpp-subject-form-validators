from edc_base.modelform_validators import FormValidator
from edc_constants.constants import OTHER


class HeartAttackFormValidator(FormValidator):

    def clean(self):
        self.m2m_other_specify(
            OTHER, m2m_field='dx_heart_attack',
            field_other='dx_heart_attack_other')
