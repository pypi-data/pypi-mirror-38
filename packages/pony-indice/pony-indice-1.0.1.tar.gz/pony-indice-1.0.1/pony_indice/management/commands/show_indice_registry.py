# TODO: Yes, yes to improve
from django.core.management.base import BaseCommand, CommandError
from pony_indice.registry import registry


class Command(BaseCommand):
    help = "Show indice registry's content"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        title = "\t\t".join([
            "Model key",
            "Display",
            "URL",
            "Description",
            "Tags",
            "Skip",
        ])
        self.stdout.write(title)
        for model, model_opts in registry.items():
            row = "\t\t".join([
                model,
                str(model_opts['display']),
                str(model_opts['url']),
                str(model_opts['description']),
                str(model_opts['tags']),
                str(model_opts['skip']),
            ])
            self.stdout.write(row)
