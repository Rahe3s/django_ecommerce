from django import forms
from . models import User_Details


# class loginForms(forms.ModelForm):
#     class Meta:
#          model = User_Details
#          fields =  [ 'phone', 'password']
#          widgets = {
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#          }
class LoginForms(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number' ,'autocomplete': 'off'}),
        max_length=15
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'})
    )

    # phone = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'})
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    # )


class regForms(forms.ModelForm):
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password', 'autocomplete': 'new-password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User_Details  
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']  

        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name','autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name','autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number','autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email','autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
