from edc_base.modelform_validators.form_validator import FormValidator


class ResourceUtilizationFormValidator(FormValidator):

    def clean(self):
        money_spent = self.cleaned_data.get('money_spent')
        if money_spent:
            self.required_if_true(
                money_spent > 0,
                field_required='medical_cover')
