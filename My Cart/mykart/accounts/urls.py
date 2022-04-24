from django.urls import path,include
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
#     path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('forgotpassword', views.forgotpassword,name='forgotpassword'),
    # path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword_validate/<uid>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    
    path('resetPassword', views.resetPassword,name="resetPassword")
]