from django.forms import ModelForm
from django import forms

from main.models import Cartoons, CartoonsGenres, CartoonsStatus, CartoonsTypes, Studios
from .models import TempCartoon

from PIL import Image

# Create the form class.
class CartoonForm(ModelForm):
    class Meta:
        model = TempCartoon
        fields = ["eng_title", "rus_title", "description", "type", "status", "start_year", "end_year", "number_of_seasons", "number_of_series", "genres", "studios", "cover"]

    eng_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Название на английском"
    )
    rus_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Название на русском"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label="Описание"
    )
    
    type = forms.ModelChoiceField(
        queryset=CartoonsTypes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип"
    )
    status = forms.ModelChoiceField(
        queryset=CartoonsStatus.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Статус"
    )

    start_year = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label="Дата начала"
    )
    end_year = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label="Дата окончания"
    )

    number_of_seasons = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        label="Количество сезонов"
    )
    number_of_series = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        label="Количество серий"
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=CartoonsGenres.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Жанры"
    )
    studios = forms.ModelMultipleChoiceField(
        queryset=Studios.objects.all(),
        required=False,
        label="Студия"
    )

    cover = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Обложка (формат jpg, разрешение 380x562)"
    )
    

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')

        if cover:
            if not cover.name.lower().endswith('.jpg'):
                raise forms.ValidationError("Допускаются только файлы в формате JPG.")
            img = Image.open(cover)
            width, height = img.size
            if width != 380 or height != 562:
                raise forms.ValidationError("Разрешение изображения должно быть 380x562 пикселей.")

        return cover
