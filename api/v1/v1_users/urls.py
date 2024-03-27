from django.urls import re_path

from api.v1.v1_users.views import RegisterView, LoginView, UserListView

urlpatterns = [
    re_path(r'^(?P<version>(v1))/user/register/', RegisterView.as_view()),
    re_path(r'^(?P<version>(v1))/user/login/', LoginView.as_view()),
    re_path(r'^(?P<version>(v1))/user/list/', UserListView.as_view()),
]
