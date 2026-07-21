from django import forms
from .models import Event
from clients.models import Client


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['client', 'person_name', 'relation', 'event_type', 'event_date']
        widgets = {
            'person_name': forms.TextInput(attrs={
                'autocomplete': 'new-password',
                'autocorrect': 'off',
                'spellcheck': 'false',
            }),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'autocomplete': 'off',
            }),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields['client'].queryset = Client.objects.filter(organization=organization)