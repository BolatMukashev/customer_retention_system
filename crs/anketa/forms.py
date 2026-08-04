# anketa/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet, modelformset_factory
from .models import RewardStep


class RewardStepForm(forms.ModelForm):
    class Meta:
        model = RewardStep
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Скидка 10%'}),
        }


class BaseRewardStepFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        active_forms = [
            f for f in self.forms
            if f.cleaned_data and not f.cleaned_data.get('DELETE', False)
        ]
        total = len(active_forms)

        if not (3 <= total <= 10):
            raise ValidationError('Количество наград должно быть от 3 до 10.')

    def save(self, organization, commit=True):
        instances = []
        position = 1
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                if form.instance.pk:
                    form.instance.delete()
                continue
            instance = form.save(commit=False)
            instance.organization = organization
            instance.position = position
            position += 1
            if commit:
                instance.save()
            instances.append(instance)
        return instances


RewardStepFormSet = modelformset_factory(
    RewardStep,
    form=RewardStepForm,
    formset=BaseRewardStepFormSet,
    extra=1,
    can_delete=True,
    max_num=10,
    validate_max=True,
)