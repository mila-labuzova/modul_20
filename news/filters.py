import django_filters
from django_filters import FilterSet
from .models import Post, Author
from django import forms


class PostFilter(FilterSet):
    author = django_filters.ModelChoiceFilter(field_name='author',
                                              queryset=Author.objects.all(),
                                              empty_label='Все авторы')
    name = django_filters.CharFilter(label='Название',
                                     lookup_expr='iregex')
    date_add = django_filters.DateFilter(label='Дата добавления',
                                         lookup_expr='gt',
                                         widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
       model = Post
       fields = ['author', 'name', 'date_add']
