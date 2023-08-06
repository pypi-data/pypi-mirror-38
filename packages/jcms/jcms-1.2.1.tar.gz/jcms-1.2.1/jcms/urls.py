from django.urls import path
from jcms.components import UrlParser
from .views import loginViews

app_name = 'jcms'

urlpatterns = [
    # login views
    path('', loginViews.LoginView.as_view(), name="login"),
    path('logout/', loginViews.logout_user, name="logoutUser"),
] + UrlParser.get_urls()
