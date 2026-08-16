# events/forms.py

from django import forms
from .models import Event
from clients.models import Client
from .models import RelationType


class HiddenDateInput(forms.DateInput):
    """Как DateInput, но рендерится как <input type="hidden">.
    Нужен, чтобы Django форматировал дату по нашему формату (DD-MM-YYYY)
    вместо ISO-строки по умолчанию — это важно для предзаполнения на edit."""
    input_type = 'hidden'


class RussianEmptyChoiceMixin:
    empty_choice_fields = ('relation', 'event_type')

    def _apply_russian_empty_choice(self):
        for field_name in self.empty_choice_fields:
            field = self.fields[field_name]
            choices = list(field.choices)
            if choices and choices[0][0] == '':
                choices[0] = ('', 'Выберите вариант')
            if field_name == 'relation':
                choices = [c for c in choices if c[0] != RelationType.SELF]
            field.choices = choices


class EventForm(RussianEmptyChoiceMixin, forms.ModelForm):
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
        self._apply_russian_empty_choice()



class AnketaEventForm(RussianEmptyChoiceMixin, forms.ModelForm):
    event_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=HiddenDateInput(format='%d-%m-%Y'),
    )

    class Meta:
        model = Event
        fields = ['person_name', 'relation', 'event_type', 'event_date']
        widgets = {
            'person_name': forms.TextInput(attrs={
                'autocomplete': 'new-password',
                'autocorrect': 'off',
                'spellcheck': 'false',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_russian_empty_choice()