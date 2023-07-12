from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('page/<int:page>', views.index, name='home'),
    path('comments/<int:log>', views.log, name='comments'),
    path('<str:username>', views.user_profile, name='profile'),
    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/', views.user_logout, name='logout'),
    path('auth/signup/', views.user_signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
