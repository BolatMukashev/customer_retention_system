# forms.py
from django import forms
from organizations.models import Organization


class OrganizationSettingsForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['upcoming_event_days']
        widgets = {
            'upcoming_event_days': forms.NumberInput(attrs={'min': 1, 'max': 30}),
        }

        