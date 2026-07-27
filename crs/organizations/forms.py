from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "type", "phone", "address", "tariff"]
        labels = {
            "name": "Название организации",
            "type": "Сфера деятельности",
            "phone": "Телефон",
            "address": "Адрес",
            "tariff": "Тариф",
        }
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "+7 700 000 00 00"}),
            "address": forms.TextInput(attrs={"placeholder": "Город, улица, дом"}),
        }