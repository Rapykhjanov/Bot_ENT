from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import User as DjangoUser

class UserRegistrationView(generics.CreateAPIView):
    queryset = DjangoUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = DjangoUser.objects.create_user(**serializer.validated_data)
        # Здесь можно добавить дополнительную логику после регистрации, например, отправку email
        return Response(serializer.data, status=201)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer # Можно создать отдельный сериализатор для логина
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Здесь нужно реализовать логику аутентификации, например, создание токена
            return Response({'message': 'Успешная авторизация'}, status=200)
        else:
            return Response({'error': 'Неверные учетные данные'}, status=400)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user