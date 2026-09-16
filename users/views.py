from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsNotBanned
from .serializers import (
    RegisterSerializer, UserProfileSerializer,
    VerifySecurityAnswerSerializer, ResetPasswordSerializer,
)
from .services import verify_security_answer, generate_reset_token, verify_reset_token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsNotBanned]

    def get_object(self):
        return self.request.user


class LoginView(TokenObtainPairView):
    pass


class VerifySecurityAnswerView(APIView):
    def post(self, request):
        serializer = VerifySecurityAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=serializer.validated_data['username'])
        except User.DoesNotExist:
            return Response(
                {'detail': "Foydalanuvchi yoki javob noto'g'ri."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not verify_security_answer(user, serializer.validated_data['security_answer']):
            return Response(
                {'detail': "Foydalanuvchi yoki javob noto'g'ri."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = generate_reset_token(user)
        return Response({'reset_token': token})


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = verify_reset_token(serializer.validated_data['token'])
        if not user_id:
            return Response(
                {'detail': "Token yaroqsiz yoki muddati tugagan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=user_id)
        user.password = make_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'detail': "Parol muvaffaqiyatli yangilandi."})
        