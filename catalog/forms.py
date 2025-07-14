from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        forbidden = [w for w in FORBIDDEN_WORDS if w.lower() in name.lower()]
        if forbidden:
            raise forms.ValidationError(f"В названии обнаружены запрещённые слова: {', '.join(forbidden)}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        forbidden = [w for w in FORBIDDEN_WORDS if w.lower() in description.lower()]
        if forbidden:
            raise forms.ValidationError(f"В описании обнаружены запрещённые слова: {', '.join(forbidden)}")
        return description

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price 