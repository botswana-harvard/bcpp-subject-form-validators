from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NEG, POS, IND, DECLINED

from ..constants import NOT_PERFORMED, CAPILLARY


def neg_required_if_hic_enrollment(subject_visit=None, hiv_result=None,
                                   hic_enrollment_model=None):
    """Raises if HicEnrollment is complete for this visit and
    an attempt is made to set `hiv_result` to something other
    than NEG.
    """
    hic_enrollment_model_cls = django_apps.get_model(hic_enrollment_model)
    try:
        model_obj = hic_enrollment_model_cls.objects.get(
            subject_visit__report_datetime=subject_visit.report_datetime)
    except ObjectDoesNotExist:
        pass
    else:
        if hiv_result != NEG:
            raise forms.ValidationError({
                'hiv_result':
                'Result cannot be changed. HIC Enrollment form exists '
                f'for this subject at "{model_obj.subject_visit.visit_code}". '
                f'Got hiv_result={hiv_result}'})


class HivResultFormValidator(FormValidator):

    hic_enrollment_model = None
    subject_requisition_model = None
    microtube_panel_name = None

    def clean(self):

        neg_required_if_hic_enrollment(
            subject_visit=self.cleaned_data.get('subject_visit'),
            hiv_result=self.cleaned_data.get('hiv_result'),
            hic_enrollment_model=self.hic_enrollment_model)

        self.subject_requisition_model_cls = django_apps.get_model(
            self.subject_requisition_model)
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
