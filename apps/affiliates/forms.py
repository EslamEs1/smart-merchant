from django import forms

from .models import AffiliateProfile


class AffiliateChangeLevelForm(forms.Form):
    level = forms.ChoiceField(choices=AffiliateProfile.Level.choices)


class AffiliateNotesForm(forms.ModelForm):
    class Meta:
        model = AffiliateProfile
        fields = ["notes"]
