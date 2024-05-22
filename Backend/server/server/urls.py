#urls.py
from django.contrib import admin
from django.urls import path
from .views import CreateUserView, LoginView, SendMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', CreateUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/send-message/', SendMessageView.as_view(), name='send_message'),
]
