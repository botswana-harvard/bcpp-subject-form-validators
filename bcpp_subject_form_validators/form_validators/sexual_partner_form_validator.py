from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import DWTA, NO

from ..constants import DAYS, MONTHS, YEARS


class SexualPartnerFormValidator(FormValidator):

    sexual_behaviour_model = None
    partner_residency_model = None

    def clean(self):
        sexual_behaviour_model_cls = django_apps.get_model(
            self.sexual_behaviour_model)
        partner_residency_model_cls = django_apps.get_model(
            self.partner_residency_model)

        try:
            subject_behaviour = sexual_behaviour_model_cls.objects.get(
                subject_visit=self.cleaned_data.get('subject_visit'))
        except sexual_behaviour_model_cls.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    sexual_behaviour_model_cls._meta.verbose_name))
        else:
            if subject_behaviour.lifetime_sex_partners == 1:
                if self.cleaned_data.get('concurrent') not in [NO, DWTA]:
                    raise forms.ValidationError({
                        'concurrent': (
                            "You wrote that you have only one partner ever on {}. "
                            "Please correct if you have sex with other partners.".format(
                                sexual_behaviour_model_cls._meta.verbose_name))})

        responses = []
        for obj in partner_residency_model_cls.objects.all():
            if ('outside' in obj.short_name.lower()
                    and 'community' in obj.short_name.lower()):
                responses.append(obj.short_name)
        self.m2m_other_specify_applicable(
            *responses,
            m2m_field='first_partner_live',
            field_other='sex_partner_community')

        self.required_if(
            DAYS, MONTHS, field='third_last_sex', field_required='third_last_sex_calc')
        self.required_if(
            DAYS, MONTHS, YEARS, field='first_first_sex', field_required='first_first_sex_calc')
        self.validate_other_specify('first_relationship')
        self.validate_other_specify(
            'first_exchange_age', other_stored_value='gte_19')
