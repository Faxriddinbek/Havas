from rest_framework.views import APIView

from apps.user.serializer import UserSerializer


class UserRegisterAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)



    def get(self):
        pass