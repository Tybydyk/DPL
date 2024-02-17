from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.generic import TemplateView
from . models import Car, CarModel
from .forms import CarForm
import logging
from random import randint

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def sts(request, comments=None):
    logger.info('Car page accessed')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            model = form.cleaned_data['model']
            images = form.cleaned_data['image']
            # fs = FileSystemStorage()
            # file = fs.save(images.name, images)
            # url_file = fs.url(file)
            comments = form['comments']
            number_plate = randint(5000, 5100)
            vin = str(randint(1000, 1100))
            logger.info(f'Получили {model=}, {comments=}, {number_plate=}')
            car_in = Car(model=model, comments=comments.value(), images=images, vin=vin, number_plate=number_plate)
            car_in.save()
            message = 'Данные сохранены'
            form = CarForm()
    else:
        form = CarForm()
        message = 'Заполните форму'

    return render(request, "sts.html", {'form': form, 'message': message})
