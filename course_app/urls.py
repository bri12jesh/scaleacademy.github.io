from django.urls import path
from . import views

urlpatterns=[
    path('',views.main),
    path('course',views.course),
    path('login',views.login),
    path('logout',views.logout),
    path('signin',views.signin),
    path('user/<str:token>/', views.user, name='user'),
    path('payment',views.paymentinfo),
   path('user/<str:token>/learning/', views.learning, name='learning'),
    path('userdetail',views.userdetail),
   path('otpgenerate',views.otpgenerate),
   path('update',views.update_)

#    path('delete',views.delete_account)

    # path('logout',views.logout)
]