from django import forms

from .models import Account, Speedups


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('state', 'name', 'alliance')


class SpeedupsForm(forms.ModelForm):
    class Meta:
        model = Speedups
        fields = (
            'training_1m',
            'training_5m',
            'training_1h',
            'healing_1m',
            'healing_5m',
            'healing_1h',
            'construction_1m',
            'construction_5m',
            'construction_1h',
            'research_1m',
            'research_5m',
            'research_1h',
            'generic_1m',
            'generic_5m',
            'generic_1h',
            'generic_3h',
            'generic_8h',
        )