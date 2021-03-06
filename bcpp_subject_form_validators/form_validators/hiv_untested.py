from edc_base.modelform_validators import FormValidator

from ..complete_model_first import CompleteModelFirst


class HivUntestedFormValidator(FormValidator):

    hiv_testing_history_model = None

    def clean(self):
        CompleteModelFirst(
            subject_visit=self.cleaned_data.get('subject_visit'),
            model=self.hiv_testing_history_model)
