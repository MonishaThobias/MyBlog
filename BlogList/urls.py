from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
    path('blog/', views.blog_list, name='blog_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('subscribe/', views.subscribe_ajax, name='subscribe_ajax'),
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_email, name='validate_email'),
    path("search/", views.search, name="search"),
    
  
]