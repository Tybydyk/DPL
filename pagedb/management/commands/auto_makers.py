from django.core.management.base import BaseCommand
from pagedb.models import CarMaker


class Command(BaseCommand):
    help = "Create auto_makers."

    def handle(self, *args, **kwargs):
        lst_car_makers = []
        j = 0
        for i in range(len(lst_car_makers)):
            j += 1
            maker = CarMaker(j, lst_car_makers[i])
            maker.save()
            self.stdout.write(f'{maker}')
