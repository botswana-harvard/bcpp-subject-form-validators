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
            OTHER,
            field='tests_ordered',
            field_required='ordered_other',
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
            OTHER,
            field='medication_prescribed',
            field_required='prescribed_other',
        )

        self.required_if(
            YES,
            field='further_evaluation',
            field_required='evaluation_referred',
        )

    def validate_care_costs(self):
        sum_sort_cares = (
            self.cleaned_data.get('tb_care') +
            self.cleaned_data.get('health_related') +
            self.cleaned_data.get('health_related_none_tb') +
            self.cleaned_data.get('pregnancy_related') +
            self.cleaned_data.get('injury_accident') +
            self.cleaned_data.get('chronic_disease') +
            self.cleaned_data.get('cancer_care') +
            self.cleaned_data.get('other_care_count')
            )

        total_care_sort = self.cleaned_data.get('times_care_obtained')

        if sum_sort_cares != total_care_sort:
            raise forms.ValidationError({
                'Total of cares received must be equal to total'
                'cares declared.'}
            )

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
