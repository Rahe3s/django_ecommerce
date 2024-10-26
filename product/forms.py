from django import forms
from .models import Category,products,productImages
from django.forms import modelformset_factory,inlineformset_factory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_image']

    # Optionally, add custom validation or widgets if needed
    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        # Add any custom validation if required
        return category_name

class ProductsForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ['product_name', 'category', 'price', 'product_description']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = productImages
        fields = ['image']

ProductImageUpdateFormSet = inlineformset_factory(
    products,
    productImages,
    form = ProductImageForm,
    extra =0,
)

ProductImageFormSet = inlineformset_factory(
    products,
    productImages,
    form = ProductImageForm,
    extra =3,
)


from django import forms
from .models import ProductVariant

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'stock', 'price_adjustment']