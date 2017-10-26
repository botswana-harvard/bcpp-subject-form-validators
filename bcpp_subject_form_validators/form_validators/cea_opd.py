from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, OTHER


class CeaOpdFormValidator(FormValidator):

    def clean(self):

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

        return self.cleaned_data
