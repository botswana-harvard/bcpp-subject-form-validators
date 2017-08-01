from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NEG, POS
from django.core.exceptions import ObjectDoesNotExist


class ElisaHivResultFormValidator(FormValidator):

    hic_enrollment_model = None
    subject_requisition_model = None

    def clean(self):
        # validating that hiv_result is not changed after HicEnrollment is
        # filled.
        self.hic_enrollment_model_cls = django_apps.get_model(
            self.hic_enrollment_model)
        subject_visit = self.cleaned_data.get('subject_visit')
        try:
            model_obj = self.hic_enrollment_model_cls.objects.get(
                subject_visit__report_datetime=subject_visit.report_datetime)
        except ObjectDoesNotExist:
            pass
        else:
            hiv_result = self.cleaned_data.get('hiv_result')
            if hiv_result != NEG:
                raise forms.ValidationError({
                    'hiv_result':
                    'Result cannot be changed. HIC Enrollment form exists '
                    f'for this subject at "{model_obj.subject_visit.visit_code}". '
                    f'Got hiv_result={hiv_result}'})

        # validating that a Microtube exists before filling this form.
        self.subject_requisition_model_cls = django_apps.get_model(
            self.subject_requisition_model)
        if not self.subject_requisition_model_cls.objects.filter(panel_name='ELISA').exists():
            raise forms.ValidationError({
                'hiv_result':
                'ELISA Result cannot be saved before an ELISA Requisition is requested.'})

        self.required_if(POS, NEG, field='hiv_result',
                         field_required='hiv_result_datetime')
