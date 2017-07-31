from edc_base.modelform_validators import FormValidator
from edc_constants.constants import DWTA, OTHER


class CommunityEngagementFormValidator(FormValidator):

    def clean(self):
        self.m2m_single_selection_if(DWTA, m2m_field='problems_engagement')
        self.m2m_other_specify(
            OTHER,
            m2m_field='problems_engagement',
            field_other='problems_engagement_other')
