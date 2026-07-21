from django import forms
from .models import Order
from clients.models import Client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'amount', 'note']
        widgets = {
            'client': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={
                'autocomplete': 'off',
            }),
            'note': forms.Textarea(attrs={
                'rows': 3,
                'autocomplete': 'new-password',
            }),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields['client'].queryset = Client.objects.filter(organization=organization)