from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class EducationFormValidator(FormValidator):

    subject_locator_model = None

    def clean(self):
        self.subject_locator_model_cls = django_apps.get_model(
            self.subject_locator_model)
        subject_visit = self.cleaned_data.get('subject_visit')
        try:
            subject_locator = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_visit.subject_identifier)
        except self.subject_locator_model_cls.DoesNotExist:
            pass
        else:
            if (subject_locator.may_call_work == YES
                    and self.cleaned_data.get('working') == NO):
                raise forms.ValidationError({
                    'working':
                    'Participant gave permission to be contacted at WORK in '
                    'the subject locator but now reports to be \'Not Working\'. '
                    'Please correct.'})

        self.required_if(
            YES,
            field='working',
            field_required='job_type')

        self.required_if(
            YES,
            field='working',
            field_required='job_description')

        self.required_if(
            YES,
            field='working',
            field_required='monthly_income')

        self.required_if(
            NO,
            field='working',
            field_required='reason_unemployed')
