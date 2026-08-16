from django import forms
from .models import Client


class HiddenDateInput(forms.DateInput):
    """Рендерится как <input type="hidden"> с датой в формате DD-MM-YYYY —
    нужно для wheel-date-picker (date_linear.js)."""
    input_type = 'hidden'


class ClientForm(forms.ModelForm):
    birthday = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=HiddenDateInput(format='%d-%m-%Y'),
        required=False,
    )

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
            "note": forms.Textarea(attrs={
                "rows": 3,
                "autocomplete": "new-password",
            }),
        }