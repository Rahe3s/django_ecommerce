from django import forms
from .models import Banner

class BannerForms(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title','description','position','image']