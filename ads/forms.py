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
        
class ExchangeProposalForm(forms.ModelForm):
    """Форма для создания предложения обмена"""
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
            self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)