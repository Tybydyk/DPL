from django import forms
from .models import CarModel


class CarForm(forms.Form):
    model = forms.ModelChoiceField(label='Модель машины', empty_label='Выберите из списка',
                                     queryset=CarModel.objects.all())
    image = forms.ImageField(label='Фотография СТС')
    comments = forms.CharField(widget=forms.Textarea, label='Комментарии')
