from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from .models import Developer, Game, Platform, Publisher


class GameViewsTest(TestCase):
    """
    Test cases for game views.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = Client()
        # Example URL (seems incorrect, check)
        self.games_url = "localhost:/8001"
        self.post_games_url = "https://www.freetogame.com/api/games"

        # Create test data
        self.platform = Platform.objects.create(name="PC")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.developer = Developer.objects.create(name="Test Developer")
        self.game = Game.objects.create(
            title="Test Game",
            genre="Test Genre",
            description="Test Description",
            release_date="2023-01-01",
            platform=self.platform,
            publisher=self.publisher,
            developer=self.developer,
        )

    def test_front_page(self):
        """
        Test case for checking front page view.
        """
        response = self.client.get(reverse("front_page"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "game/front_page.html")

    @patch("requests.get")
    def test_import_games_success(self, mock_get):
        """
        Test case for successful game import via GET request.
        """
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = [
            {
                "title": "New Game",
                "genre": "New Genre",
                "short_description": "New Description",
                "release_date": "2023-01-01",
                "platform": "PC",
                "publisher": "New Publisher",
                "developer": "New Developer",
            },
        ]
        mock_get.return_value = mock_response

        response = self.client.get(reverse("import_games"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success_count", response.context)
        self.assertIn("fail_count", response.context)
        self.assertTemplateUsed(response, "game/success.html")

    @patch("requests.get")
    def test_import_games_failure(self, mock_get):
        """
        Test case for failed game import via GET request.
        """
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get.return_value = mock_response

        response = self.client.get(reverse("import_games"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "game/error.html")

    @patch("requests.post")
    def test_post_games_success(self, mock_post):
        """
        Test case for successful game posting via POST request.
        """
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_201_CREATED
        mock_post.return_value = mock_response

        response = self.client.post(reverse("post_games"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "game/post.html")
        self.assertIn("success_count", response.context)
        self.assertIn("fail_count", response.context)

    @patch("requests.post")
    def test_post_games_failure(self, mock_post):
        """
        Test case for failed game posting via POST request.
        """
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_post.return_value = mock_response

        response = self.client.post(reverse("post_games"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "game/post.html")
