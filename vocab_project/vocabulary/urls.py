
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/',  views.registration.as_view(), name='registration'),
    path('accounts/login/',views.login_view, name ="login"),
    path('logout/', views.custom_logout, name='logout'),
    path('full_page/<int:pk>/', views.full_page, name='full_page'),
    path('search/', views.search, name='search'),
    path('basic/', views.basic, name='basic'),
    path('intermediate/', views.intermediate, name='intermediate'),
    path('advanced/', views.advanced, name='advanced'),
    path('SaveItems/', views.SaveItems, name = "SaveItems"),
    path('delete-container/', views.DeleteContainer, name='delete_container'),
    path('SaveWord/', views.SaveWord, name='SaveWord'),
    path('onebox/<str:container>/', views.onebox, name='onebox'),
    path('Delete/<str:container_name>/<int:pk>/', views.DeleteWordFormContainer, name ='Delete'),
    path('APISection', views.APISection.as_view(), name='APISection'),
    path('ApiPlan/', views.ApiPlan.as_view(), name='ApiPlan'),
    path('AddCoaching/', views.AddCoaching, name='AddCoaching',),
    path("Coaching/", views.Coaching, name="Coaching"),
    path('UpdateCoachingData/', views.UpdateCoachingData, name='UpdateCoachingData'), 
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
