from django.db import models

from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.utils import get_utcnow


class SubjectVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25, default='T0')


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    may_call_work = models.CharField(max_length=25)
