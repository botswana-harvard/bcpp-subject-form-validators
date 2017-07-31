from arrow.arrow import Arrow
from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase, tag

from edc_base.modelform_validators import REQUIRED_ERROR, NOT_REQUIRED_ERROR
from edc_constants.constants import MALE, YES, NO, NOT_APPLICABLE, OTHER, DWTA
from edc_registration.models import RegisteredSubject

from ..form_validators import HivCareAdherenceFormValidator
from .models import SubjectVisit, ListModel


class TestHivCareAdherence(TestCase):

    def setUp(self):
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            gender=MALE)
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier)

    def test_none(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            diagnoses=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_no_medical_care_applicable(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            medical_care=NO,
            no_medical_care=NOT_APPLICABLE)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('no_medical_care', form_validator._errors)

    def test_no_medical_care_other(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            medical_care=NO,
            no_medical_care=OTHER,
            no_medical_care_other=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('no_medical_care_other', form_validator._errors)

    def test_not_ever_taken_arv_applicable(self):
        for response in [NO, DWTA]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=response,
                    why_no_arv=NOT_APPLICABLE)
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('why_no_arv', form_validator._errors)

    def test_ever_taken_arv_applicable(self):
        for field in ['on_arv', 'arv_evidence']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=YES,
                    **{field: NOT_APPLICABLE})
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(field, form_validator._errors)

    def test_ever_taken_arv_required(self):
        for field in ['first_arv']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=YES,
                    **{field: NOT_APPLICABLE})
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(field, form_validator._errors)
                self.assertIn(REQUIRED_ERROR,
                              form_validator._error_codes)

    def test_first_arv_date_not_before_first_positive(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_arv=(Arrow.utcnow() - relativedelta(years=1)).datetime,
            first_positive=Arrow.utcnow().datetime)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('first_arv', form_validator._errors)

    def test_first_arv_date_equal_first_positive(self):
        dt = Arrow.utcnow()
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_arv=dt.datetime,
            first_positive=dt.datetime)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('first_arv', form_validator._errors)

    def test_first_arv_date_lt_first_positive(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_arv=Arrow.utcnow().datetime,
            first_positive=(Arrow.utcnow() - relativedelta(years=1)).datetime)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('first_arv', form_validator._errors)

    def test_on_arv_requires_arv_stop_date(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_arv=Arrow.utcnow().datetime,
            on_arv=YES,
            arv_stop_date=Arrow.utcnow().datetime,
        )
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arv_stop_date', form_validator._errors)
        self.assertIn(NOT_REQUIRED_ERROR,
                      form_validator._error_codes)

    def test_arv_stop_date_not_before_first_arv(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_arv=Arrow.utcnow().datetime,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=(
                Arrow.utcnow() - relativedelta(years=1)).datetime)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arv_stop_date', form_validator._errors)

    def test_arv_stop_date_equal_first_arv(self):
        dt = Arrow.utcnow() - relativedelta(years=1)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            on_arv=NO,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            first_arv=dt.datetime,
            arv_stop_date=dt)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('arv_stop_date', form_validator._errors)

    def test_arv_stop_date_gt_first_arv(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            on_arv=NO,
            first_positive=(Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=(Arrow.utcnow() - relativedelta(months=1)).datetime)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertNotIn('arv_stop_date', form_validator._errors)

    def test_arvs_not_required_on_arv_is_NO(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        ListModel.objects.create(short_name='arv2', name='arv12')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=(
                Arrow.utcnow() - relativedelta(months=1)).datetime,
            on_arv=NO,
            arvs=ListModel.objects.all())
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arvs', form_validator._errors)

    def test_arvs_not_required_if_on_arv_is_DWTA(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        ListModel.objects.create(short_name='arv2', name='arv12')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            on_arv=DWTA,
            arvs=ListModel.objects.all())
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arvs', form_validator._errors)

    def test_arvs_applicable_and_required_if_on_arv(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        ListModel.objects.create(
            short_name=NOT_APPLICABLE, name=NOT_APPLICABLE)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            on_arv=YES,
            arvs=ListModel.objects.all())
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arvs', form_validator._errors)

    def test_arvs_required_if_on_arv(self):
        for arvs in [None, ListModel.objects.all()]:
            with self.subTest(arvs=arvs):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=YES,
                    first_positive=(
                        Arrow.utcnow() - relativedelta(years=2)).datetime,
                    first_arv=(
                        Arrow.utcnow() - relativedelta(years=1)).datetime,
                    on_arv=YES,
                    arvs=arvs)
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('arvs', form_validator._errors)

    def test_arvs_other_required(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        ListModel.objects.create(
            short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            on_arv=YES,
            arvs=ListModel.objects.all())
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('arv_other', form_validator._errors)

    def test_on_arv_is_first_regimen_is_required(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        for response in [None, ListModel.objects.filter(name='blah')]:
            with self.subTest(response=response):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=YES,
                    first_positive=(
                        Arrow.utcnow() - relativedelta(years=2)).datetime,
                    first_arv=(
                        Arrow.utcnow() - relativedelta(years=1)).datetime,
                    arv_stop_date=(
                        Arrow.utcnow() - relativedelta(months=1)).datetime,
                    on_arv=NO,
                    arvs=response,
                    is_first_regimen=YES)
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn('is_first_regimen', form_validator._errors)

    def test_not_on_arv_prev_is_not_required(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        for field in ['prev_switch_date', 'prev_arvs', 'prev_arv_other']:
            with self.subTest(field=field):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    ever_taken_arv=YES,
                    first_positive=(
                        Arrow.utcnow() - relativedelta(years=2)).datetime,
                    first_arv=(
                        Arrow.utcnow() - relativedelta(years=1)).datetime,
                    arv_stop_date=(
                        Arrow.utcnow() - relativedelta(months=1)).datetime,
                    on_arv=NO,
                    arvs=None,
                    is_first_regimen=None,
                    **{field: YES})
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(field, form_validator._errors)

    def test_on_arv_is_first_regimen_prev_not_required(self):
        """Asserts if on arv and regimen is not the current one,
        prev data is not required."
        """
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.all(),
            is_first_regimen=YES,
            prev_switch_date=None,
            prev_arvs=ListModel.objects.all())
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('prev_arvs', form_validator._errors)

    def test_prev_OTHER_required(self):
        """Assert prev_arv_other required because is not the first
        regimen and one of prev_arvs is OTHER.
        """
        ListModel.objects.create(short_name='arv1', name='arv1')
        ListModel.objects.create(short_name=OTHER, name=OTHER)
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=5)).datetime,
            prev_arvs=ListModel.objects.all(),
            prev_arv_other=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('prev_arv_other', form_validator._errors)

    def test_prev_switch_date_cannot_preceded_first_arv(self):
        """Assert if not first regimen then switch date cannot precede
        first_arv date.
        """
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=5)).datetime,
            prev_arvs=ListModel.objects.all(),
            prev_arv_other=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('prev_switch_date', form_validator._errors)

    def test_prev_switch_required_if_not_first_regimen(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=None,
            prev_arvs=ListModel.objects.all(),
            prev_arv_other=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('prev_switch_date', form_validator._errors)

    def test_adherence(self):
        """Assert if not first regimen then switch date cannot precede
        first_arv date.
        """
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=3)).datetime,
            prev_arvs=ListModel.objects.all(),
            adherence_4_day=NOT_APPLICABLE)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('adherence_4_day', form_validator._errors)

    def test_hospitalization_applicable(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=3)).datetime,
            prev_arvs=ListModel.objects.all(),
            adherence_4_day=YES,
            ever_taken_arv=YES,
            hospitalized_art_start=NOT_APPLICABLE)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hospitalized_art_start', form_validator._errors)

    def test_hospitalization_duration(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=3)).datetime,
            prev_arvs=ListModel.objects.all(),
            adherence_4_day=YES,
            ever_taken_arv=YES,
            hospitalized_art_start=YES)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hospitalized_art_start_duration',
                      form_validator._errors)

    def test_hospitalization_reason(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            arv_stop_date=None,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=NO,
            first_arv=(Arrow.utcnow() - relativedelta(months=4)).datetime,
            prev_switch_date=(
                Arrow.utcnow() - relativedelta(months=3)).datetime,
            prev_arvs=ListModel.objects.all(),
            adherence_4_day=YES,
            ever_taken_arv=YES,
            hospitalized_art_start=YES,
            hospitalized_art_start_duration=3,
            hospitalized_art_start_reason=NOT_APPLICABLE)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hospitalized_art_start_reason',
                      form_validator._errors)

    def test_hospitalization_reasons(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        options = dict(
            chronic_disease='chronic_disease',
            medication_toxicity='medication_toxicity',
            **{OTHER: 'hospitalized_art_start_reason_other'})
        for reason, field_required in options.items():
            with self.subTest(reason=reason):
                cleaned_data = dict(
                    subject_visit=self.subject_visit,
                    first_positive=(
                        Arrow.utcnow() - relativedelta(years=2)).datetime,
                    arv_stop_date=None,
                    on_arv=YES,
                    arvs=ListModel.objects.filter(name='arv1'),
                    is_first_regimen=NO,
                    first_arv=(Arrow.utcnow() -
                               relativedelta(months=4)).datetime,
                    prev_switch_date=(
                        Arrow.utcnow() - relativedelta(months=3)).datetime,
                    prev_arvs=ListModel.objects.all(),
                    adherence_4_day=YES,
                    ever_taken_arv=YES,
                    hospitalized_art_start=YES,
                    hospitalized_art_start_duration=3,
                    hospitalized_art_start_reason=reason)
                form_validator = HivCareAdherenceFormValidator(
                    cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except forms.ValidationError:
                    pass
                self.assertIn(field_required, form_validator._errors)

    def test_hospitalized_evidence(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=YES,
            hospitalized_art_start=YES,
            hospitalized_art_start_duration=3,
            hospitalized_art_start_reason='something')
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('hospitalized_evidence', form_validator._errors)

    def test_clinic(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            on_arv=YES,
            arvs=ListModel.objects.filter(name='arv1'),
            is_first_regimen=YES,
            clinic_receiving_from=None)
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('clinic_receiving_from', form_validator._errors)

    def test_clinic_not_required(self):
        ListModel.objects.create(short_name='arv1', name='arv1')
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            on_arv=NO,
            ever_taken_arv=YES,
            first_positive=(
                Arrow.utcnow() - relativedelta(years=2)).datetime,
            first_arv=(
                Arrow.utcnow() - relativedelta(years=1)).datetime,
            arv_stop_date=(
                Arrow.utcnow() - relativedelta(months=1)).datetime,
            clinic_receiving_from='i am not required')
        form_validator = HivCareAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('clinic_receiving_from', form_validator._errors)
