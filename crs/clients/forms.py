from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'telegram', 'birthday', 'note']
        widgets = {
            "name": forms.TextInput(attrs={
                "autocomplete": "new-password",
                "autocorrect": "off",
                "spellcheck": "false",
            }),
            "phone": forms.TextInput(attrs={
                "autocomplete": "new-password",
            }),
            "telegram": forms.TextInput(attrs={
                "autocomplete": "new-password",
                "autocorrect": "off",
                "spellcheck": "false",
            }),
            "birthday": forms.DateInput(attrs={
                "type": "date",
                "autocomplete": "off",
            }),
            "note": forms.Textarea(attrs={
                "rows": 3,
                "autocomplete": "new-password",
            }),
        }
        labels = {
            "birthday": "День рождения",
        }