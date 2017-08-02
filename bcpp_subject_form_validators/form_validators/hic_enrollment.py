from bcpp_status import StatusHelper
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base.modelform_validators import FormValidator
from edc_base.utils import age
from edc_constants.constants import YES, NO, NEG, IND

from ..complete_model_first import CompleteModelFirst


class HicEnrollmentFormValidator(FormValidator):

    status_helper_cls = StatusHelper
    subject_consent_model = 'bcpp_subject.subjectconsent'
    subject_locator_model = 'bcpp_subject.subjectlocator'
    residency_mobility_model = 'bcpp_subject.residencymobility'
    hiv_result_model = 'bcpp_subject.hivresult'
    elisa_hiv_result_model = 'bcpp_subject.elisahivresult'

    def clean(self):

        subject_consent = CompleteModelFirst(
            subject_identifier=self.cleaned_data.get(
                'subject_visit').subject_identifier,
            model=self.subject_consent_model).model_obj

        subject_locator = CompleteModelFirst(
            subject_identifier=self.cleaned_data.get(
                'subject_visit').subject_identifier,
            model=self.subject_locator_model).model_obj

        if self.cleaned_data.get('hic_permission') == NO:
            raise forms.ValidationError(
                {'hic_permission': 'Subject is not eligible'})
        elif self.cleaned_data.get('hic_permission') == YES:
            self.validate_age(subject_consent)
            self.validate_residency()
            self.validate_is_hiv_negative()
            self.validate_citizenship(subject_consent)
            self.validate_subject_locator(subject_locator)

    def validate_age(self, subject_consent):
        consent_age = age(
            subject_consent.dob, subject_consent.consent_datetime)
        if not 16 <= consent_age.years <= 64:
            raise forms.ValidationError(
                f'Invalid age. Got {consent_age.years}. See consent.',
                code='invalid_age')

    def validate_residency(self):
        model_obj = CompleteModelFirst(
            subject_visit=self.cleaned_data.get('subject_visit'),
            model=self.residency_mobility_model).model_obj
        if not model_obj.permanent_resident == YES:
            raise forms.ValidationError(
                f'Please review \'permanent_resident\'. See {self.residency_mobility_model}.',
                code='invalid_residency')

    def validate_is_hiv_negative(self):
        hiv_result_model_cls = django_apps.get_model(self.hiv_result_model)
        elisa_hiv_result_model_cls = django_apps.get_model(
            self.elisa_hiv_result_model)
        try:
            hiv_result = hiv_result_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'))
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f'Please complete {hiv_result_model_cls._meta.verbose_name} first.',
                code='missing_hiv_result')
        if hiv_result.hiv_result == IND:
            try:
                elisa_hiv_result_model_cls.objects.get(
                    subject_visit=self.cleaned_data.get('subject_visit'))
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    f'Please complete {elisa_hiv_result_model_cls._meta.verbose_name} first.',
                    code='missing_elisa_hiv_result')
        status_helper = self.status_helper_cls(
            visit=self.cleaned_data.get('subject_visit'))
        if status_helper.final_hiv_status != NEG:
            raise forms.ValidationError(
                'Please review \'hiv_result\' in Today\'s Hiv '
                'Result form or in Elisa Hiv Result before '
                f'proceeding. Got final_hiv_status={status_helper.final_hiv_status}',
                code='invalid_hiv_status')

    def validate_citizenship(self, subject_consent):
        # Raise an error if not a citizen or married to a citizen.
        if not ((subject_consent.citizen == YES) or (
                subject_consent.legal_marriage == YES and
                subject_consent.marriage_certificate == YES)):
            raise forms.ValidationError(
                'Please review \'citizen\', \'legal_marriage\' and '
                f'\'marriage_certificate\' in SubjectConsent for {subject_consent}. '
                f'Got citizen={subject_consent.citizen}, '
                f'legal_marriage={subject_consent.legal_marriage}, '
                f'marriage_certificate={subject_consent.marriage_certificate}',
                code='invalid_citizenship')

    def validate_subject_locator(self, subject_locator):
            # Raise an error if subject locator is not completed.
        if not (subject_locator.subject_cell or
                subject_locator.subject_cell_alt or
                subject_locator.subject_phone or
                subject_locator.mail_address or
                subject_locator.physical_address or
                subject_locator.subject_cell or
                subject_locator.subject_cell_alt or
                subject_locator.subject_phone or
                subject_locator.subject_phone_alt or
                subject_locator.subject_work_place or
                subject_locator.subject_work_phone or
                subject_locator.contact_physical_address or
                subject_locator.contact_cell or
                subject_locator.contact_phone):
            raise forms.ValidationError(
                'Please review Subject Locator to ensure there is some '
                'way to contact the participant form before '
                'proceeding.', code='invalid_locator')
