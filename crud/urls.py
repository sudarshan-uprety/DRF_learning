from django.urls import path
from . import views
from .views import RegisterView,PostView,LoginView,UserProfileView,ChangePasswordView


app_name="task"
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('posts/',PostView.as_view(),name='post'),
    path('changepassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('posts/<int:pk>',PostView.as_view(),name='post_details'),

]