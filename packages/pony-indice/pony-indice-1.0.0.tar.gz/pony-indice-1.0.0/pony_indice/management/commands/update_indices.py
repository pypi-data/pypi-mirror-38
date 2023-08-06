from django.core.management.base import BaseCommand, CommandError
from pony_indice.registry import registry
from pony_indice import utils

MODEL_CHOICES = {
    '%s.%s' % (m._meta.app_label, m._meta.model_name): m
    for m in registry.models
}

class Command(BaseCommand):
    help = "Create or update links from your existing database."

    def add_arguments(self, parser):
        parser.add_argument(
            dest='models',
            help='Models to update.',
            nargs='*',
            choices=list(MODEL_CHOICES.keys())+['all']),

    def handle(self, *args, **options):
        models = MODEL_CHOICES if 'all' in options['models'] else options['models']
        for model_name in models:
            model_class = MODEL_CHOICES[model_name]
            options = registry.get_model_options(model_class)
            queryset = model_class.objects.all()
            for instance in queryset:
                utils.create_or_update_link(instance, model_class, options)
            self.stdout.write(self.style.SUCCESS(
                'OK\t: %s' % model_class._meta.verbose_name))
