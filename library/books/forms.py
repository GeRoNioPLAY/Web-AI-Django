from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']
        labels = {
            'title': 'Название',
            'author': 'Автор',
            'price': 'Цена'
        }

class BookFilterForm(forms.Form):
    title = forms.CharField(max_length=200, required=False, label='Название')
    author = forms.ChoiceField(choices=[], required=False, label='Автор')
    price_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Минимальная цена', widget=forms.NumberInput(attrs={'step': '0.01'}))
    price_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Максимальная цена', widget=forms.NumberInput(attrs={'step': '0.01'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        authors = Book.objects.values_list('author', flat=True).distinct()
        self.fields['author'].choices = [('', 'Все авторы')] + [(author, author) for author in authors]