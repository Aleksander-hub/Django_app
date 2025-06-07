from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from . import views

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('create/', views.create, name='create'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='index'), name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('advertisements/add/', views.add_advertisement, name='add_advertisement'),
    path('advertisements/edit/<int:pk>/', views.edit_advertisement, name='edit_advertisement'),
    path('advertisements/delete/<int:pk>/', views.delete_advertisement, name='delete_advertisement'),
]

