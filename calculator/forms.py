from django import forms
from .models import WasteInput

class WasteInputForm(forms.ModelForm):
    class Meta:
        model = WasteInput
        fields = ['waste_type', 'quantity_kg', 'latitude', 'longitude', 'location_name']
        widgets = {
            'waste_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500'}),
             'location_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_location_name', 'placeholder': 'Click map to load address...'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_longitude'}),
        }