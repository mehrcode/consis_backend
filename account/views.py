from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework.permissions import (
    AllowAny,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")

        if password1 != password2:
            return Response({"error": "password does not match"}, status=400)

        data = {
            "email": email,
            "password": password1,
        }
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=201)

        return Response({"error": serializer.errors}, status=400)
