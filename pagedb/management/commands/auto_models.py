from django.core.management.base import BaseCommand
from pagedb.models import CarModel


class Command(BaseCommand):
    help = "Create auto_odelss."

    def handle(self, *args, **kwargs):
        lst_car_models = []
        j = 0
        for el in lst_car_models:
            j += 1
            model = CarModel(j, el[1], int(el[0]))
            model.save()
            self.stdout.write(f'{model}')
