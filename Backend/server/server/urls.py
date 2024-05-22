from django.contrib import admin
from django.urls import path
from .views import CreateUserView, LoginView, SendMessageView, UserListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', CreateUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/send-message/', SendMessageView.as_view(), name='send_message'),
    path('api/users/', UserListView.as_view(), name='user_list'),  # Nueva ruta para obtener la lista de usuarios
]
