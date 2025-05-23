from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from requests import get, post
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user_auth.models import User
from user_auth.throttling import AuthUserRateThrottle

from core.save_image import save_image


class GoogleLoginView(APIView):
    """API endpoint for generating Google sign-in URL."""

    throttle_classes = [AuthUserRateThrottle]

    def get(self, request) -> Response:
        # Define google auth URL
        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

        # Setting up google auth URL params
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }

        # Build google sign in url
        login_url = f"{google_auth_url}?{urlencode(params)}"

        # Return google sign in url
        return success_response(
            message="Google sign-in URL successfully generated",
            data={
                "signin_url": login_url,
            },
        )


class GoogleTokenExchangeView(APIView):
    """API endpoint for exchanging Google authorization code for an access token."""

    throttle_classes = [AuthUserRateThrottle]

    def get(self, request) -> Response:
        """Exchange authorization code for an access token."""

        # Get google code from request
        auth_code = request.GET.get("code")

        # Validate auth google code
        if not auth_code:
            return failure_response(
                message="Access token retrieval failed",
                errors={"code": ["Google authorization code was not found."]},
            )

        # Define google code to token exchage URL
        token_url = "https://oauth2.googleapis.com/token"

        # Define google required data
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

        # Send request to Google to exchange code for a token
        response = post(token_url, data=data)
        token_data = response.json()

        # Check access_token is not token_data
        if "access_token" not in token_data:
            return failure_response(
                message="Google access token retrieval failed",
                errors={"code": ["Access token not present in Google's response."]},
            )

        # Return success response
        return success_response(
            message="Google access token successfully retrieved",
            data={"token": token_data["access_token"]},
        )


class GoogleCallbackView(APIView):
    """API endpoint for handling Google sign-in callback."""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request) -> Response:
        """Verify Google token (ID token or access token)."""

        # Get google token from request
        token = request.data.get("token")

        # Validate google token
        if not token:
            return failure_response(
                message="Google authentication token missing",
                errors={"token": ["A valid authentication token is required."]},
            )

        try:
            # Define google data
            google_data = {}

            # Try to verify as an ID Token first
            try:
                google_data = id_token.verify_oauth2_token(
                    token, requests.Request(), settings.GOOGLE_CLIENT_ID
                )
            except ValueError:
                # If that fails, treat it as an OAuth access token and fetch user info
                google_user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
                headers = {"Authorization": f"Bearer {token}"}
                response = get(google_user_info_url, headers=headers)

                # Check request status
                if response.status_code != 200:
                    return failure_response(
                        message="Invalid authentication token",
                        errors={
                            "token": [
                                "The authentication token is invalid or has expired."
                            ]
                        },
                    )

                # Convert response instance to json
                google_data = response.json()

            print("============================")
            print("Google Data: ", google_data)
            print("============================")

            # Extract user details
            email = google_data.get("email")
            # profile_picture = google_data.get("picture")

            # Check user email is valid or not
            if not email:
                return failure_response(
                    message="Invalid authentication token",
                    errors={
                        "token": ["The authentication token is invalid or has expired."]
                    },
                )

            # Handle user profile picture
            # picture = save_image(User, "picture", profile_picture, email)

            # Save user and generate JWT tokens
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": google_data.get("given_name"),
                    "last_name": google_data.get("family_name"),
                    # "picture": picture,
                    "is_verified": True,
                },
            )

            # Update user details if they already exist
            user.first_name = google_data.get("given_name")
            user.last_name = google_data.get("family_name")
            # setattr(user, "picture", picture)
            setattr(user, "is_verified", True)
            user.save()

            """Generate JWT tokens using Simple JWT."""
            refresh = RefreshToken.for_user(user)

            # Getting the access token from refresh token
            access_token = getattr(refresh, "access_token", None)

            # Checking if access token is None or not
            if access_token is None:
                return failure_response(
                    message="Failed to generate access token",
                    errors={"token": ["Failed to generate access token."]},
                )

            # Update last login timestamp
            if user:
                setattr(user, "last_login", timezone.now())
                user.save(update_fields=["last_login"])

            # Return success response
            return success_response(
                message="Google sign-in completed successfully",
                data={
                    "refresh_token": str(refresh),
                    "access_token": str(access_token),
                },
            )
        except Exception as error:
            print("============================")
            print(error)
            print("============================")

            # Return failure response
            return failure_response(
                message="Google authentication failed",
                errors={"detail": "Somethings is wrong!. Please try again."},
            )
