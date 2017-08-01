from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO

from ..constants import ZERO


class ResidencyMobilityFormValidator(FormValidator):

    hic_enrollment_model = None

    def clean(self):
        # validating that residency status is not changed after capturing
        # enrollment checklist
        self.hic_enrollment_model_cls = django_apps.get_model(
            self.hic_enrollment_model)
        try:
            self.hic_enrollment_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'))
        except ObjectDoesNotExist:
            pass
        else:
            if (self.cleaned_data.get('permanent_resident') != YES
                    or self.cleaned_data.get('intend_residency') != NO):
                raise forms.ValidationError(
                    'An HicEnrollment form exists for this '
                    'subject. Values for \'permanent_resident\''
                    ' and \'intend_residency\' cannot be changed.'
                    f'Got permanent_resident={self.cleaned_data.get("permanent_resident")}, '
                    f'intend_residency={self.cleaned_data.get("intend_residency")}.'
                )

        # validating residency + nights away. redmine 126
        if (self.cleaned_data.get('permanent_resident') == YES and
                self.cleaned_data.get('nights_away') == 'more than 6 months'):
            raise forms.ValidationError({
                'nights_away':
                'Participant has spent 14 or more nights per month '
                'in this community, nights away can\'t be '
                'more than 6 months.'})

        self.not_applicable_if(
            ZERO, field='nights_away', field_applicable='cattle_postlands')
        self.validate_other_specify(
            'cattle_postlands', other_stored_value='Other community')
