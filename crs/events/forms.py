from django import forms
from .models import Event
from clients.models import Client


class HiddenDateInput(forms.DateInput):
    """Как DateInput, но рендерится как <input type="hidden">.
    Нужен, чтобы Django форматировал дату по нашему формату (DD-MM-YYYY)
    вместо ISO-строки по умолчанию — это важно для предзаполнения на edit."""
    input_type = 'hidden'


class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=HiddenDateInput(format='%d-%m-%Y'),
    )

    class Meta:
        model = Event
        fields = ['client', 'person_name', 'relation', 'event_type', 'event_date']
        widgets = {
            'client': forms.HiddenInput(),
            'person_name': forms.TextInput(attrs={
                'autocomplete': 'new-password',
                'autocorrect': 'off',
                'spellcheck': 'false',
            }),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields['client'].queryset = Client.objects.filter(organization=organization)