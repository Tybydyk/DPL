from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import Car
from .forms import CarForm
import logging
from random import randint
from .ocr_module import image_to_text

logger = logging.getLogger(__name__)


@login_required
def sts(request, comments=None):
    logger.info('Car page accessed')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            model = form.cleaned_data['model']
            images = form.cleaned_data['image']
            comments = form['comments']
            number_plate = f'номер {randint(10, 100)}'
            vin = f'VIN {randint(10, 100)}'
            logger.info(f'Получили {model=}, {comments=}, {number_plate=}')
            car_in = Car(model=model, comments=comments.value(), images=images, vin=vin, number_plate=number_plate)
            car_in.save()
            print(car_in.images.path)
            car_in.number_plate, car_in.vin, car_in.year, car_in.color = image_to_text(car_in.images.path)
            car_in.save()
            return redirect('index')
    else:
        form = CarForm()
        message = 'Заполните форму'
    return render(request, "sts.html", {'form': form, 'message': message})
