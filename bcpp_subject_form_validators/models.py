from django.conf import settings

if settings.APP_NAME == 'bcpp_subject_form_validators':

    from .tests import ReferenceConfigHelper
    from edc_reference.site import site_reference_configs
    from pprint import pprint

    reference_config_helper = ReferenceConfigHelper()
    reference_config_helper.reconfigure('bcpp_subject_form_validator')

    pprint(site_reference_configs.registry)

    from .tests.models import *
