from django import forms
from .models import Car, CarModel


class CarForm(forms.Form):
    model = forms.ModelChoiceField(label='Car model', empty_label='Please select',
                                     queryset=CarModel.objects.all())
    image = forms.ImageField()
    comments = forms.CharField(widget=forms.Textarea)
