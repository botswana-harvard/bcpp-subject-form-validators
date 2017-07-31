from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class SubjectLocatorFormValidator(FormValidator):

    hic_enrollment_model = None

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):

        self.validate_has_contacts_for_hic()
        self.required_if(
            YES, field='home_visit_permission', field_required='physical_address')
        self.required_if(
            YES, field='may_follow_up', field_required='subject_cell')
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_cell_alt', inverse=False)
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_phone', inverse=False)
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_phone_alt', inverse=False)

    def validate_has_contacts_for_hic(self):
        self.hic_enrollment_model_cls = django_apps.get_model(
            self.hic_enrollment_model)
        try:
            model_obj = self.hic_enrollment_model_cls.objects.get(
                subject_visit__subject_identifier=self.cleaned_data.get(
                    'subject_identifier'))
        except self.hic_enrollment_model_cls.DoesNotExist:
            pass
        else:
            if (not model_obj.subject_cell and not model_obj.subject_cell_alt
                    and not model_obj.subject_phone):
                raise forms.ValidationError(
                    'Subject is enrolled to HIC. Please provide at least one '
                    'contact number.')
