from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import User, Image, Interaction

class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"mobile_number": "1234567890", "name": "Test User"}

    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            self.user_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        otp = response.data["message"].split("-")[-1]
        self.user_data["otp"] = otp
        response = self.client.post(
            reverse("register"),
            self.user_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserLoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(mobile_number="1234567890", name="Test User")

    def test_login_user(self):
        response = self.client.post(
            reverse("login"),
            {"mobile_number": self.user.mobile_number},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        otp = response.data["message"].split("-")[-1]
        response = self.client.post(
            reverse("login"),
            {"mobile_number": self.user.mobile_number, "otp": otp},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class HomeViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_images(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class InteractionViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(mobile_number="1234567890", name="Test User")
        self.image = Image.objects.create(url="http://example.com/image.jpg", name="Test Image")

    def test_post_interaction(self):
        response = self.client.post(
            reverse("interaction"),
            {"user": self.user.id, "image": self.image.id, "action": "accept"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class HistoryViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(mobile_number="1234567890", name="Test User")

    def test_get_history(self):
        response = self.client.get(reverse("history", kwargs={"user_id": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
