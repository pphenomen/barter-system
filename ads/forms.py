from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    """Форма для создания объявления"""
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'condition': forms.Select(),
        }