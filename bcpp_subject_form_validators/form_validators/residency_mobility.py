from django import forms
from django.apps import apps as django_apps

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES

from ..constants import ZERO


class ResidencyMobilityFormValidator(FormValidator):

    residency_mobility_model = None

    def clean(self):
        self.residency_mobility_model_cls = django_apps.get_model(
            self.residency_mobility_model)
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = self.residency_mobility_model_cls(**self.cleaned_data)
        # validating that residency status is not changed after capturing
        # enrollment checklist
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating residency + nights away. redmine 126
        if (self.cleaned_data.get('permanent_resident') == YES and
                self.cleaned_data.get('nights_away') == 'more than 6 months'):
            raise forms.ValidationError({
                'nights_away':
                'Participant has spent 14 or more nights per month '
                'in this community, nights away can\'t be '
                'more than 6 months.'})

        self.not_applicable_if(ZERO, 'nights_away', 'cattle_postlands')
        self.validate_other_specify(
            'cattle_postlands', other_stored_value='Other community')
