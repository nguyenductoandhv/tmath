from django import forms

from typeracer.models import TypoRoom


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = TypoRoom
        fields = ['name', 'is_private', 'access_code']

    def clean_access_code(self):
        if self.cleaned_data['is_private'] and not self.cleaned_data['access_code']:
            raise forms.ValidationError("Access code is required")
        return self.cleaned_data['access_code']
