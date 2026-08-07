from django import forms
from .models import Application, TariffType


class TariffSelect(forms.Select):
    """Select, в котором опция 'Премиум' недоступна для выбора."""

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value == TariffType.PREMIUM:
            option["attrs"]["disabled"] = "disabled"
        return option


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
            "tariff": TariffSelect(),
        }

    def clean_tariff(self):
        tariff = self.cleaned_data.get("tariff")
        if tariff == TariffType.PREMIUM:
            raise forms.ValidationError("Тариф «Премиум» пока недоступен для подключения.")
        return tariff