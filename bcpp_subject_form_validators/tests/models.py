from django.db import models

from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_base.model_mixins.list_model_mixin import ListModelMixin
from edc_appointment.models import Appointment


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

    subject_visit = models.ForeignKey(SubjectVisit)

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.subject_visit.visit_code


class SexualBehaviour(CrfModelMixin, BaseUuidModel):

    ever_sex = models.CharField(max_length=25)
