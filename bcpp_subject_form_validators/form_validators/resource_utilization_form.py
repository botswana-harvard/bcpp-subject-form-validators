from django import forms

from ..models import ResourceUtilization
from .form_mixins import SubjectModelFormMixin


class ResourceUtilizationFormValidator(FormValidator):

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('money_spent') and not cleaned_data.get('medical_cover'):
            if (cleaned_data.get('money_spent') > 0):
                raise forms.ValidationError(
                    'If money was spent on medicines, were all of these '
                    'covered by anyone else e.g. medical aid?')

        return cleaned_data

    class Meta:
        model = ResourceUtilization
        fields = '__all__'
