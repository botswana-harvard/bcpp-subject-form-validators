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
            raise forms.ValidationError({
                'first_arv':
                'Cannot be before {}.'.format(
                    self.cleaned_data.get('first_positive').strftime('%Y-%m-%d'))})

        self.required_if(
            NO, field='on_arv', field_required='arv_stop_date')

        if (self.cleaned_data.get('arv_stop_date') and self.cleaned_data.get('first_arv')
                and self.cleaned_data.get('arv_stop_date') <= self.cleaned_data.get('first_arv')):
            raise forms.ValidationError({
                'arv_stop_date':
                'Cannot be before {}'.format(
                    self.cleaned_data.get('first_arv').strftime('%Y-%m-%d'))})
        self.validate_other_specify('arv_stop')

    def validate_art_regimen(self, m2m_field=None, field_other=None):
        m2m_field = m2m_field or 'arvs'
        field_other = field_other or 'arv_other'
        if (self.cleaned_data.get('on_arv') == [NO, DWTA]
                and self.cleaned_data.get(m2m_field)):
            raise forms.ValidationError({
                m2m_field:
                'This field is not required.'})
        elif self.cleaned_data.get('on_arv') == YES:
            if self.cleaned_data.get(m2m_field):
                if (self.cleaned_data.get(m2m_field).count() == 0):
                    raise forms.ValidationError({
                        m2m_field:
                        'This field is required. Please make a selection.'})
                elif (self.cleaned_data.get(m2m_field).count() > 0):
                    for obj in self.cleaned_data.get(m2m_field):
                        if obj.short_name == NOT_APPLICABLE:
                            raise forms.ValidationError({
                                m2m_field:
                                'Invalid selection. Cannot be not applicable.'})
                        elif obj.short_name == OTHER and not self.cleaned_data.get(field_other):
                            raise forms.ValidationError({
                                field_other:
                                'This field is required.'})
            elif not self.cleaned_data.get(m2m_field):
                raise forms.ValidationError({
                    m2m_field:
                    'This field is required. Please make a selection.'})

    def validate_prev_art_regimen(self):
        self.validate_is_first_regimen()
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

    def validate_is_first_regimen(self):
        self.required_if(
            YES, field='on_arv', field_required='is_first_regimen')
        if (self.cleaned_data.get('on_arv') == [NO, DWTA]
                and not self.cleaned_data.get('is_first_regimen')):
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
        if self.cleaned_data.get('on_arv') == YES:
            if self.cleaned_data.get('adherence_4_day') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_day':
                    'This field is applicable'})
            elif self.cleaned_data.get('adherence_4_wk') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'This field is applicable'})
        elif self.cleaned_data.get('on_arv') in [NO, DWTA]:
            if self.cleaned_data.get('adherence_4_day') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_day':
                    'This field is not applicable'})
            elif self.cleaned_data.get('adherence_4_wk') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'This field is not applicable'})

    def validate_hospitalization_part1(self):
        if self.cleaned_data.get('hospitalized_art_start') == YES:
            if self.cleaned_data.get('ever_taken_arv') in [NO, DWTA]:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is not applicable'})
            elif not self.cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is required'})
            elif self.cleaned_data.get('hospitalized_art_start_reason') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is applicable'})
        elif self.cleaned_data.get('hospitalized_art_start') == NO:
            if self.cleaned_data.get('ever_taken_arv') in [NO, DWTA]:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is not applicable'})
            elif self.cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is not required'})
            elif self.cleaned_data.get('hospitalized_art_start_reason') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is not applicable'})
        elif self.cleaned_data.get('hospitalized_art_start') == NOT_APPLICABLE:
            if self.cleaned_data.get('ever_taken_arv') == YES:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is applicable'})
            elif self.cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is not required'})
            elif self.cleaned_data.get('hospitalized_art_start_reason') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is not applicable'})

    def validate_hospitalization_part2(self):
        if self.cleaned_data.get('hospitalized_art_start_reason'):
            if self.validate_other_specify('hospitalized_art_start_reason'):
                pass
            elif (self.cleaned_data.get('hospitalized_art_start_reason') == 'chronic_disease'
                    and not self.cleaned_data.get('chronic_disease')):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is required'})
            elif (self.cleaned_data.get('hospitalized_art_start_reason') != 'chronic_disease'
                  and self.cleaned_data.get('chronic_disease')):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is not required'})
            elif (self.cleaned_data.get('hospitalized_art_start_reason') == 'medication_toxicity'
                  and not self.cleaned_data.get('medication_toxicity')):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is required'})
            elif (self.cleaned_data.get('hospitalized_art_start_reason') != 'medication_toxicity'
                  and self.cleaned_data.get('medication_toxicity')):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is not required'})
        elif not self.cleaned_data.get('hospitalized_art_start_reason'):
            if self.cleaned_data.get('chronic_disease'):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is not required'})
            elif self.cleaned_data.get('medication_toxicity'):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is not required'})

    def validate_hospitalization_part3(self):
        if self.cleaned_data.get('hospitalized_art_start') == YES:
            if not self.cleaned_data.get('hospitalized_evidence'):
                raise forms.ValidationError({
                    'hospitalized_evidence':
                    'This field is required'})
            elif self.validate_other_specify('hospitalized_evidence'):
                pass
        elif self.cleaned_data.get('hospitalized_art_start') == NO:
            if self.cleaned_data.get('hospitalized_evidence'):
                raise forms.ValidationError({
                    'hospitalized_evidence':
                    'This field is not required'})

    def validate_clinic(self):
        if (self.cleaned_data.get('on_arv') == YES
                and not self.cleaned_data.get('clinic_receiving_from')):
            raise forms.ValidationError({
                'clinic_receiving_from':
                'This field is required'})
        elif (self.cleaned_data.get('on_arv') == [NO, DWTA]
              and self.cleaned_data.get('clinic_receiving_from')):
            raise forms.ValidationError({
                'clinic_receiving_from':
                'This field is not required'})
        elif (self.cleaned_data.get('clinic_receiving_from')
              and not self.cleaned_data.get('next_appointment_date')):
            raise forms.ValidationError({
                'next_appointment_date':
                'This field is required'})
        elif (not self.cleaned_data.get('clinic_receiving_from')
              and self.cleaned_data.get('next_appointment_date')):
            raise forms.ValidationError({
                'next_appointment_date':
                'This field is not required'})
