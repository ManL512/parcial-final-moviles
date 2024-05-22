# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import jwt
from .models import User, Message, FCMToken
from .serializers import UserSerializer, LoginSerializer, MessageSerializer
from firebase_admin import messaging

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['password'] = make_password(data['password'])
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = User.objects.get(email=serializer.data['email'])

            # Save the FCM token
            fcm_token = data.get('fcm_token')
            if fcm_token:
                FCMToken.objects.create(user=user, token=fcm_token)

            # Create JWT token
            payload = {'email': serializer.data['email']}
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            response_data = serializer.data
            response_data['token'] = token

            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.data['email'])
                if check_password(serializer.data['password'], user.password):
                    # Verifica si existe un token FCM en la solicitud
                    fcm_token = request.data.get('fcm_token', None)

                    # Guarda el nuevo token FCM si no existe o es diferente
                    if fcm_token and (not user.fcm_token or user.fcm_token != fcm_token):
                        user.fcm_token = fcm_token
                        user.save()

                        # Si el usuario ya tiene un token asociado, lo actualizamos
                        if FCMToken.objects.filter(user=user).exists():
                            FCMToken.objects.filter(user=user).update(token=fcm_token)
                        else:
                            FCMToken.objects.create(user=user, token=fcm_token)

                    return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(sender=request.user)
            recipient_tokens = FCMToken.objects.filter(user=message.recipient).values_list('token', flat=True)
            response = self.send_push_notification(recipient_tokens, message.title, message.body)
            message.recipient_token = recipient_tokens
            message.firebase_response = response
            message.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_push_notification(self, tokens, title, body):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        return response
