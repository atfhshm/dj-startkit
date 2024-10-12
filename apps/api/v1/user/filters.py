from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import rest_framework as drf

from apps.user.models import User

__all__ = [
    "UserFilter",
]


class UserFilter(drf.FilterSet):
    o = drf.OrderingFilter(fields=(("id", "id"), ("date_joined", "date_joined")))
    name = drf.CharFilter(method="filter_name", label="name")
    email = drf.CharFilter(field_name="email", lookup_expr="icontains")
    username = drf.CharFilter(field_name="username", lookup_expr="icontains")
    phone_number = drf.CharFilter(field_name="phone_number", lookup_expr="icontains")

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
        )

    def filter_name(self, queryset, name, value):
        return queryset.annotate(
            name=Concat("first_name", Value(" "), "last_name")
        ).filter(name__icontains=value)
