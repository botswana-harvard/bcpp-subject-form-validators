from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, OTHER
from django import forms


class CeaOpdFormValidator(FormValidator):

    def clean(self):

        self.validate_care_costs()

        self.required_if(
            YES,
            field='lab_tests_ordered',
            field_required='tests_ordered',
        )

        self.required_if(
            YES,
            field='procedures_performed',
            field_required='procedure',
        )

        self.required_if(
            YES,
            field='medication',
            field_required='medication_prescribed',
        )

        self.required_if(
            YES,
            field='further_evaluation',
            field_required='evaluation_referred',
        )

    def validate_care_costs(self):
        if (self.cleaned_data.get('other_care') and not
           (self.cleaned_data.get('other_care_count'))):
            raise forms.ValidationError({
                'other_care_count': 'This field is required'
            })

        if (not self.cleaned_data.get('other_care') and
           (self.cleaned_data.get('other_care_count'))):
            raise forms.ValidationError({
                'other_care_count': 'This field is not required'
            })
