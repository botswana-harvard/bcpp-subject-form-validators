from django import forms

from ..constants import ANNUAL
from ..models import ReproductiveHealth
from .form_mixins import SubjectModelFormMixin


class ReproductiveHealthFormValidator(FormValidator):

    optional_attrs = {ANNUAL: {
        'label': {'family_planning': (
            'Since we spoke with you at our last visit, have you used any methods'
            'to prevent pregnancy?')}}}

    def clean(self):
        cleaned_data = super().clean()
        if ((cleaned_data.get('when_pregnant') and cleaned_data.get('when_pregnant') == 'No') and
            (cleaned_data.get('gestational_weeks') or
             (cleaned_data.get('pregnancy_hiv_tested') != 'N/A' or
              cleaned_data.get('pregnancy_hiv_retested') != 'N/A'))):
            raise forms.ValidationError(
                'If participant did not get pregnant since last interview, then do not'
                'provide answers for \
                questions from "At about what gestational age (in weeks) did you start'
                'arv\'s during this '
                '(or your last) pregnancy?"')
        if cleaned_data.get('menopause') == 'Yes' and cleaned_data.get('family_planning'):
            raise forms.ValidationError(
                'if participant has reached menopause, you should not be giving details about'
                'family planning')
        if cleaned_data.get('menopause') == 'Yes' and cleaned_data.get('currently_pregnant'):
            raise forms.ValidationError(
                'If participant has reached menopause, do not give details about current pregnancy')
        if cleaned_data.get('menopause') == 'No' and not cleaned_data.get('family_planning'):
            raise forms.ValidationError(
                'if participant has not reached menopause, provide the family planning details')
        if cleaned_data.get('menopause') == 'No' and not cleaned_data.get('currently_pregnant'):
            raise forms.ValidationError(
                'If participant has not reached menopause, we need '
                'to know if participant is currently pregnant or not.')
        return cleaned_data

    class Meta:
        model = ReproductiveHealth
        fields = '__all__'
