from django.urls import path

from apps.api.v1.user.views import (
    GetCurrentUserView,
    PasswordChangeView,
    RetrieveUpdateDestroyUserView,
    UserListView,
)

urlpatterns = [
    path(
        "me",
        GetCurrentUserView.as_view(),
        name="get-auth-user",
    ),
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
