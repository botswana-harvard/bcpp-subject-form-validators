from django.db import models
from django.db.models.deletion import PROTECT

from edc_appointment.models import Appointment
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.model_mixins.list_model_mixin import ListModelMixin
from edc_base.utils import get_utcnow


class HouseholdMember(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    age_in_years = models.IntegerField(null=True)


class SubjectVisit(BaseUuidModel):

    appointment = models.ForeignKey(Appointment, null=True)

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25, default='T0')

    household_member = models.ForeignKey(HouseholdMember, null=True)

    class Meta:
        ordering = ['report_datetime']


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    may_call_work = models.CharField(max_length=25)


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class CrfModelMixin(models.Model):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.subject_visit.visit_code


class SubjectRequisition(CrfModelMixin, BaseUuidModel):

    panel_name = models.CharField(max_length=25)


class SexualBehaviour(CrfModelMixin, BaseUuidModel):

    ever_sex = models.CharField(max_length=25)


class ElisaHivResult(CrfModelMixin, BaseUuidModel):

    hiv_result = models.CharField(max_length=25)


class HivCareAdherence(CrfModelMixin, BaseUuidModel):

    pass


class HicEnrollment(CrfModelMixin, BaseUuidModel):

    hiv_result = models.CharField(max_length=25)

    def __str__(self):
        return (f'{self.subject_visit.subject_identifier} '
                f'{self.subject_visit.report_datetime} {self.subject_visit.visit_code}')
