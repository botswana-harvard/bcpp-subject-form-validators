from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES


class HivLinkageToCareFormValidator(FormValidator):

    hiv_care_adherence_model = 'bcpp_subject.hivcareadherence'

    def clean(self):
        self.hiv_care_adherence_model_cls = django_apps.get_model(
            self.hiv_care_adherence_model)
        try:
            self.hiv_care_adherence_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'))
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f'Complete {self.hiv_care_adherence_model_cls._meta.verbose_name}.')

        self.required_if_true(
            self.cleaned_data.get('kept_appt') in [
                'attended_different_clinic', 'went_different_clinic'],
            field_required='different_clinic')

        self.required_if(
            'failed_attempt', field='kept_appt', field_required='failed_attempt_date')

        self.validate_other_specify('evidence_referral')

        self.required_if(
            YES, field='recommended_art', field_required='reason_recommended_art')

        self.validate_other_specify('reason_recommended_art')

        self.required_if(
            YES, field='initiated', field_required='initiated_date')
        self.required_if(
            YES, field='initiated', field_required='initiated_clinic')
        self.required_if(
            YES, field='initiated', field_required='initiated_clinic_community')
        self.required_if(
            YES, field='initiated', field_required='evidence_art')

        self.validate_other_specify('evidence_art')
