import django_filters
from . import models
class SocietyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.society
        fields = ['society_title']
        lookup_expr = 'icontains'