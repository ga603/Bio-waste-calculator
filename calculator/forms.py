from django import forms
from .models import WasteInput

class WasteInputForm(forms.ModelForm):
    class Meta:
        model = WasteInput
        fields = ['waste_type', 'quantity_kg']
        widgets = {
            'waste_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),        }