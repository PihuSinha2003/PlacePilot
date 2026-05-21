from django.urls import path

from .views import CustomLoginView, profile_view, signup

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
]
