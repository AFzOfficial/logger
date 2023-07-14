from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('page/<int:page>', views.index, name='home'),

    path('log/like/<int:id>', views.log_like, name='like'),
    path('log/comments/<int:id>', views.log, name='comments'),
    
    path('<str:username>', views.account_profile, name='profile'),
    path('<str:username>/page/<int:page>', views.account_profile, name='profile'),

    path('<str:username>/followers', views.user_followers, name='followers'),
    path('<str:username>/followers/page/<int:page>', views.user_followers, name='followers'),

    path('<str:username>/followings', views.user_followings, name='followings'),
    path('<str:username>/followings/page/<int:page>', views.user_followings, name='followings'),

    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/signup/', views.signup_user, name='signup'),

    path('account/update/profile', views.update_profile, name='update_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
