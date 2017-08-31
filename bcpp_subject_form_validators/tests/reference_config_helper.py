from edc_reference.site import site_reference_configs


class ReferenceConfigHelper:

    def reconfigure(self, app_label=None):
        new_references = []
        for model, reference in site_reference_configs.registry.items():
            reference.model = f'{app_label}.{model.split(".")[1]}'
            new_references.append(reference)
        site_reference_configs.registry = {}
        site_reference_configs.loaded = False
        for reference in new_references:
            site_reference_configs.register(reference)
