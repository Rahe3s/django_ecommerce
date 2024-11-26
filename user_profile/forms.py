from django import forms
from accounts.models import User_Details  # Use your custom user model

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User_Details
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }