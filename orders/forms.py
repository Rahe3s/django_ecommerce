from django import forms
from . models import Coupons

class CouponForm(forms.ModelForm):
    
   
    class Meta:
        model = Coupons  
        fields = ['name', 'description', 'min_amount','discount']  

        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coupon_name','autocomplete': 'off'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description','autocomplete': 'off'}),
            'min_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'minimum amount','autocomplete': 'off'}),
        }

