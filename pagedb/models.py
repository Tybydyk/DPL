from django.core.validators import DecimalValidator
from django.db import models


class CarMaker(models.Model):
    car_maker = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.car_maker}'


class CarModel(models.Model):
    car_model = models.CharField(max_length=32)
    car_maker = models.ForeignKey(CarMaker, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car_maker.car_maker}, {self.car_model}'


class Owner(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=64, unique=True, blank=True)
    contact_data = models.TextField(blank=True, null=True)
    dating_date = models.DateField(auto_now_add=True)
    discount = models.SmallIntegerField(default=0)

    def __str__(self):
        return (f'{self.name}, {self.phone}, {self.discount} %,'
                f'\n{self.contact_data}')


STATUS_OCR = [('YES', 'Text recognition has been performed'),
              ('NO', 'It was not recognized')]


class Car(models.Model):
    vin = models.CharField(max_length=17, default='XXXXXXXXXXXXXXXXX', unique=True)
    number_plate = models.CharField(max_length=12, default='A123AA198', unique=True,)
    model = models.ForeignKey(CarModel,  default='4', on_delete=models.CASCADE)
    year = models.CharField(max_length=4, default='2020')
    color = models.CharField(max_length=32, default='Unknown')
    owner = models.ForeignKey(Owner, default='1', on_delete=models.CASCADE,)
    images = models.ImageField(upload_to='%Y-%m-%d/', blank=True, null=True)
    ocr = models.CharField(choices=STATUS_OCR, max_length=5, default='NO')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f'Car: {self.model.car_maker} {self.model.car_model}, year: {self.year}, color: {self.color},'
                f'owner: {self.owner.name}, phone: {self.owner.phone}')


class Provider(models.Model):
    provider_name = models.CharField(max_length=128)
    provider_inn = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    dating_date = models.DateField(auto_now_add=True)
    contact_person = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    contact_data = models.TextField(default='')
    contact_person_2 = models.CharField(max_length=64, null=True, blank=True)
    phone_2 = models.CharField(max_length=64, null=True, blank=True)
    contact_data_2 = models.TextField(default='')
    comments = models.TextField(default='')

    def __str__(self):
        return (f'{self.provider_name}, {self.provider_inn},'
                f'\n{self.contact_person}, {self.phone},'
                f'\n{self.contact_data}\n')


class Spare(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    part_number = models.CharField(max_length=32, blank=True)
    spare_name = models.CharField(max_length=128)
    comments = models.TextField(blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    price_from = models.DecimalField(null=False, decimal_places=2,
                                     max_digits=10, validators=[DecimalValidator(10, 2)])
    price_for = models.DecimalField(null=False, decimal_places=2,
                                     max_digits=10, validators=[DecimalValidator(10, 2)])

    def __str__(self):
        return (f'{self.spare_name}, '
                f'\n{self.part_number},'
                f'\n{self.provider}'
                f'\n{self.price_for}\n')


STATUS_CHOICES = [('IN_WORK', 'in working'),
                  ('FOR_ISSUE', 'ready to be issued'),
                  ('FINISHED', 'finished'),
                  ('CANCELED', 'canceled')]


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    spare_part = models.ForeignKey(Spare, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    date_ordered = models.DateField(auto_now_add=True)
    date_issue = models.DateField(max_length=8, blank=True)
    price_for_buyer = models.DecimalField(null=False, decimal_places=2,
                                          max_digits=10, validators=[DecimalValidator(10, 2)])
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='IN_WORK')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f'Order for spare:'
                f'\n{self.spare_part.spare_name},'
                f'\n{self.spare_part.part_number}, {self.quantity},'
                f'\n {self.price_for_buyer} roubles')
