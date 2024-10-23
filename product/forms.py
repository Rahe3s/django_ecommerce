from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_image']

    # Optionally, add custom validation or widgets if needed
    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        # Add any custom validation if required
        return category_name
