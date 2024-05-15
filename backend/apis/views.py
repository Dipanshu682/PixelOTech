from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
import random

class UserRegistration(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        name = request.data.get('name')
        otp = request.data.get('otp')

        if not otp:
            otp = random.randint(1000, 9999)
            self.request.session['otp'] = otp
            print(otp)
            return Response({"message": f"OTP has been sent to your mobile number.-{otp}"}, status=status.HTTP_200_OK)
        else:
            if self.request.session.get('otp') == int(otp):
                user = User.objects.create(mobile_number=mobile_number, name=name)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')

        if not otp:
            otp = random.randint(1000, 9999)
            self.request.session['otp'] = otp
            print(otp)
            return Response({"message": f"OTP has been sent to your mobile number.-{otp}"}, status=status.HTTP_200_OK)
        else:
            if self.request.session.get('otp') == int(otp):
                try:
                    user = User.objects.get(mobile_number=mobile_number)
                except User.DoesNotExist:
                    return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
                return Response({"message": f"Welcome {user.name}!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

class InteractionView(APIView):
    def post(self, request):
        serializer = InteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=serializer.validated_data['user'].id)
            image = Image.objects.get(id=serializer.validated_data['image'].id)
            action = serializer.validated_data['action']
            message = f'{user.name}, you have {"selected" if action == "accept" else "rejected"} image {image.name}'
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    def get(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        interactions = Interaction.objects.filter(user=user)
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)
