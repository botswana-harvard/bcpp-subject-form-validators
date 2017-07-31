from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NEG, POS, IND, DECLINED

from ..constants import NOT_PERFORMED, CAPILLARY


class HivResultFormValidator(FormValidator):

    hic_enrollment_model = None
    subject_requisition_model = None
    microtube_panel_name = None

    def clean(self):
        self.hic_enrollment_model_cls = django_apps.get_model(
            self.hic_enrollment_model)
        self.subject_requisition_model_cls = django_apps.get_model(
            self.subject_requisition_model)

        try:
            self.hic_enrollment_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'))
        except self.hic_enrollment_model_cls.DoesNotExist:
            pass
        else:
            if self.cleaned_data.get('hiv_result') != NEG:
                raise forms.ValidationError(
                    'Result cannot be changed. {} exists for this subject. '
                    'Got {0}'.format(self.hic_enrollment_model_cls._meta.verbose_name,
                                     self.cleaned_data.get('hiv_result')))

        try:
            self.subject_requisition_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'),
                panel_name=self.microtube_panel_name)
        except self.subject_requisition_model_cls.DoesNotExist:
            if self.cleaned_data.get('hiv_result') not in [DECLINED, NOT_PERFORMED]:
                raise forms.ValidationError(
                    'Please complete Microtube Requisition first.')

        self.required_if(
            POS, NEG, IND, field='hiv_result', field_required='hiv_result_datetime')

        self.applicable_if(
            POS, NEG, IND, field='hiv_result', field_applicable='blood_draw_type')
        self.applicable_if(
            CAPILLARY, field='blood_draw_type', field_applicable='insufficient_vol')

        self.required_if(
            DECLINED, NOT_PERFORMED, field='hiv_result', field_required='why_not_tested')
