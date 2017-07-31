from django.db import models

from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_base.model_mixins.list_model_mixin import ListModelMixin


class SubjectVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25, default='T0')


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    may_call_work = models.CharField(max_length=25)


class Diagnoses(ListModelMixin, BaseUuidModel):

    pass


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class CircumcisionBenefits(ListModelMixin, BaseUuidModel):
    pass


class CrfModelMixin(models.Model):

    subject_visit = models.ForeignKey(SubjectVisit)

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.subject_visit.visit_code


class MedicalDiagnoses(CrfModelMixin, BaseUuidModel):

    diagnoses = models.ManyToManyField(
        Diagnoses,
        verbose_name=(
            'Do you recall or is there a record of having any of the '
            'following serious illnesses?'),
    )
