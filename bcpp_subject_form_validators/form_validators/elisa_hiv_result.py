from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import NEG, POS

from .hiv_result import neg_required_if_hic_enrollment


class ElisaHivResultFormValidator(FormValidator):

    hic_enrollment_model = None
    subject_requisition_model = None

    def clean(self):
        # validating that hiv_result is not changed after HicEnrollment is
        # filled.
        neg_required_if_hic_enrollment(
            subject_visit=self.cleaned_data.get('subject_visit'),
            hiv_result=self.cleaned_data.get('hiv_result'),
            hic_enrollment_model=self.hic_enrollment_model)

        # validating that a Microtube exists before filling this form.
        self.subject_requisition_model_cls = django_apps.get_model(
            self.subject_requisition_model)
        if not self.subject_requisition_model_cls.objects.filter(panel_name='ELISA').exists():
            raise forms.ValidationError({
                'hiv_result':
                'ELISA Result cannot be saved before an ELISA Requisition is requested.'})

        self.required_if(POS, NEG, field='hiv_result',
                         field_required='hiv_result_datetime')
