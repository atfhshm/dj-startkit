from django.urls import path

from apps.api.v1.user.views import (
    PasswordChangeView,
    RetrieveUpdateDestroyUserView,
    UserListView,
)

urlpatterns = [
    path(
        "<str:email>",
        RetrieveUpdateDestroyUserView.as_view(),
        name="user-crud",
    ),
    path(
        "",
        UserListView.as_view(),
        name="list-users",
    ),
    path(
        "change-password",
        PasswordChangeView.as_view(),
        name="change-password",
    ),
]
