from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('page/<int:page>', views.index, name='home'),

    path('users/search/', views.search_user, name='search_user'),
    # path('logs/search/', views.search_log, name='search_log'),

    path('logs/<int:id>', views.log, name='log'),
    path('logs/<int:id>/page/<int:page>', views.log, name='log'),

    path('logs/like/<int:id>', views.log_like, name='like'),
    path('logs/delete/<int:id>', views.delete_log, name='delete_log'),
    path('logs/edit/<int:id>', views.edit_log, name='edit_log'),

    path('<str:username>', views.account_profile, name='profile'),
    path('<str:username>/page/<int:page>',
         views.account_profile, name='profile'),

    path('<str:username>/followers', views.user_followers, name='followers'),
    path('<str:username>/followers/page/<int:page>',
         views.user_followers, name='followers'),

    path('<str:username>/followings', views.user_followings, name='followings'),
    path('<str:username>/followings/page/<int:page>',
         views.user_followings, name='followings'),

    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/signup/', views.signup_user, name='signup'),

    path('accounts/profile/update/', views.update_profile, name='update_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
