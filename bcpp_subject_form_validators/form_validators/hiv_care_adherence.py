from django import forms

from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, DWTA
from edc_base.modelform_validators.form_validator import FormValidator


class HivCareAdherenceFormValidator(FormValidator):

    def clean(self):
        # section: care
        self.applicable_if(
            NO, field='medical_care', field_applicable='no_medical_care')
        self.validate_other_specify('no_medical_care')
        self.applicable_if(
            NO, DWTA, field='ever_taken_arv', field_applicable='why_no_arv')
        self.validate_other_specify('why_no_arv')

        self.validate_art_part1()

        self.required_if(
            NO, field='on_arv', field_required='arv_stop_date')
        self.applicable_if_true(
            self.cleaned_data.get('arv_stop_date'), field_applicable='arv_stop')
        self.validate_art_regimen()
        self.validate_is_first_regimen()
        self.validate_prev_art_regimen()
        self.validate_adherence()
        self.validate_hospitalization_part1()
        self.validate_hospitalization_part2()
        self.validate_hospitalization_part3()
        self.validate_clinic()

    def validate_art_part1(self):
        """Validations for first part of section Antiretiroviral
        Therapy.
        """
        self.applicable_if(
            YES, field='ever_taken_arv', field_applicable='on_arv')
        self.applicable_if(
            YES, field='ever_taken_arv', field_applicable='arv_evidence')
        self.required_if(
            YES, field='ever_taken_arv', field_required='first_arv')

        if (self.cleaned_data.get('first_positive') and self.cleaned_data.get('first_arv')
                and self.cleaned_data.get('first_positive') > self.cleaned_data.get('first_arv')):
            dt = self.cleaned_data.get('first_positive').strftime('%Y-%m-%d')
            raise forms.ValidationError({
                'first_arv': f'Cannot be before {dt}.'})

        self.required_if(
            NO, field='on_arv', field_required='arv_stop_date')

        if (self.cleaned_data.get('arv_stop_date') and self.cleaned_data.get('first_arv')
                and self.cleaned_data.get('arv_stop_date') <= self.cleaned_data.get('first_arv')):
            dt = self.cleaned_data.get('first_arv').strftime('%Y-%m-%d')
            raise forms.ValidationError({
                'arv_stop_date': f'Cannot be before {dt}'})
        self.validate_other_specify('arv_stop')

    def validate_art_regimen(self, m2m_field=None, field_other=None):
        m2m_field = m2m_field or 'arvs'
        field_other = field_other or 'arv_other'
        if (self.cleaned_data.get('on_arv') in [NO, DWTA]
                and self.cleaned_data.get(m2m_field)):
            raise forms.ValidationError({
                m2m_field: 'This field is not required.'})
        elif self.cleaned_data.get('on_arv') == YES:
            if self.cleaned_data.get(m2m_field):
                if (self.cleaned_data.get(m2m_field).count() > 0):
                    for obj in self.cleaned_data.get(m2m_field):
                        if obj.short_name == NOT_APPLICABLE:
                            raise forms.ValidationError({
                                m2m_field:
                                'Invalid selection. Cannot be not applicable.'})
                        elif obj.short_name == OTHER and not self.cleaned_data.get(field_other):
                            raise forms.ValidationError({
                                field_other: 'This field is required.'})
            elif not self.cleaned_data.get(m2m_field):
                raise forms.ValidationError({
                    m2m_field: 'This field is required. Please make a selection.'})

    def validate_is_first_regimen(self):
        self.required_if(
            YES, field='on_arv', field_required='is_first_regimen')
        if (self.cleaned_data.get('on_arv') in [NO, DWTA]
                and not self.cleaned_data.get('is_first_regimen')):
            self.prev_art_regimen_not_required()

    def validate_prev_art_regimen(self):
        if self.cleaned_data.get('is_first_regimen') == NO:
            if not self.cleaned_data.get('prev_switch_date'):
                raise forms.ValidationError({
                    'prev_switch_date':
                    'This field is required.'})
            elif (self.cleaned_data.get('prev_switch_date') and self.cleaned_data.get('first_arv')
                  and self.cleaned_data.get('prev_switch_date') <= self.cleaned_data.get('first_arv')):
                raise forms.ValidationError({
                    'prev_switch_date':
                    'Date cannot be on or before {}. (See ART start date above)'.format(
                        self.cleaned_data.get('first_arv').strftime('%Y-%m-%d'))})
            else:
                self.validate_art_regimen('prev_arvs', 'prev_arv_other')
        elif self.cleaned_data.get('is_first_regimen') == YES:
            self.prev_art_regimen_not_required()

    def prev_art_regimen_not_required(self):
        if self.cleaned_data.get('prev_switch_date'):
            raise forms.ValidationError({
                'prev_switch_date':
                'This field is not required.'})
        elif self.cleaned_data.get('prev_arvs'):
            raise forms.ValidationError({
                'prev_arvs':
                'This field is not required.'})
        elif self.cleaned_data.get('prev_arv_other'):
            raise forms.ValidationError({
                'prev_arv_other':
                'This field is not required.'})

    def validate_adherence(self):
        self.applicable_if(
            YES, field='on_arv', field_applicable='adherence_4_day')
        self.not_applicable_if(
            NO, DWTA, NOT_APPLICABLE, field='on_arv', field_applicable='adherence_4_day')

    def validate_hospitalization_part1(self):
        self.applicable_if(
            YES, field='ever_taken_arv', field_applicable='hospitalized_art_start')
        self.required_if(
            YES, field='hospitalized_art_start', field_required='hospitalized_art_start_duration')
        self.applicable_if(
            YES, field='hospitalized_art_start', field_applicable='hospitalized_art_start_reason')

    def validate_hospitalization_part2(self):
        if self.cleaned_data.get('hospitalized_art_start_reason'):
            if self.validate_other_specify('hospitalized_art_start_reason'):
                pass
            self.required_if(
                'chronic_disease', field='hospitalized_art_start_reason',
                field_required='chronic_disease')
            self.required_if(
                'medication_toxicity', field='hospitalized_art_start_reason',
                field_required='medication_toxicity')

    def validate_hospitalization_part3(self):
        self.required_if(
            YES, field='hospitalized_art_start',
            field_required='hospitalized_evidence')
        self.validate_other_specify('hospitalized_evidence')

    def validate_clinic(self):
        self.required_if(
            YES, field='on_arv',
            field_required='clinic_receiving_from')
        self.required_if_true(
            self.cleaned_data.get('clinic_receiving_from'),
            field_required='next_appointment_date')
