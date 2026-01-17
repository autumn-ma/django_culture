import importlib

from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "common"

    modules_to_initialize = [
        "common.lookups",
    ]

    def ready(self):
        for module in self.modules_to_initialize:
            importlib.import_module(module)
