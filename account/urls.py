from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('search/', views.search_number_admin, name="search_number_admin"),
    path('login/', views.login_user_view, name="login_user"),
    path('logout/', views.logout_user_view, name="logout_user"),
]