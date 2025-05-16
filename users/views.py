from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
from .serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = DjangoUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        # Создаём пользователя через create_user
        DjangoUser.objects.create_user(**serializer.validated_data)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer  # Лучше создать отдельный LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({'message': 'Успешная авторизация'}, status=200)
        else:
            return Response({'error': 'Неверные учетные данные'}, status=400)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
