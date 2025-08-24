from typing import Any
from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from requests import get, post
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.accounts.throttling import AuthUserRateThrottle


class GoogleLoginView(APIView):
    """API endpoint for generating Google sign-in URL."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012

    def get(self, request: Request) -> Response:  # noqa: ARG002
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
        return Response(
            data={"signin_url": login_url},
            status=status.HTTP_200_OK,
        )


class GoogleTokenExchangeView(APIView):
    """API endpoint for exchanging Google authorization code for an access token."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012

    def get(self, request: Request) -> Response:
        """Exchange authorization code for an access token."""
        auth_code = request.GET.get("code")

        # Validate auth google code
        if not auth_code:
            raise ValidationError({"code": "This field is required."})

        # Define google code to token exchage URL
        token_url = "https://oauth2.googleapis.com/token"  # noqa: S105

        # Define google required data
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

        # Send request to Google to exchange code for a token
        response = post(token_url, data=data, timeout=10)
        token_data = response.json()

        # Check access_token is not token_data
        if "access_token" not in token_data:
            raise ValidationError(
                {"detail": "Failed to retrieve access token from Google."}
            )

        # Return success response
        return Response(
            data={"access_token": token_data["access_token"]},
            status=status.HTTP_200_OK,
        )


class GoogleCallbackView(APIView):
    """API endpoint for handling Google sign-in callback."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012

    def post(self, request: Request) -> Response:
        """Verify Google token (ID token or access token)."""
        token = request.data.get("token")

        # Validate google token
        if not token:
            raise ValidationError({"token": "This field is required."})

        try:
            google_data: dict[str, Any] = {}

            # Try to verify as an ID Token first
            try:
                google_data = id_token.verify_oauth2_token(  # type: ignore  # noqa: PGH003
                    token,
                    requests.Request(),
                    settings.GOOGLE_CLIENT_ID,
                )
            except ValueError:
                # If that fails, treat it as an OAuth access token and fetch user info
                google_user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
                headers = {"Authorization": f"Bearer {token}"}
                response = get(google_user_info_url, headers=headers, timeout=10)

                # Check request status
                if response.status_code != 200:  # noqa: PLR2004
                    return Response(
                        data={"detail": "Failed to fetch user info from Google."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Convert response instance to json
                google_data = response.json()

            # Extract user details
            email = google_data.get("email")

            # Check user email is valid or not
            if not email:
                return Response(
                    data={"detail": "Failed to retrieve email from Google."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_data = {
                "first_name": google_data.get("given_name"),
                "last_name": google_data.get("family_name"),
                "is_verified": google_data.get("email_verified", False),
            }

            # Save user and generate JWT tokens
            user, _ = User.objects.get_or_create(
                email=email,
                defaults=user_data,
            )

            # Always update the user with latest info
            for field, value in user_data.items():
                setattr(user, field, value)

            user.save()

            """Generate JWT tokens using Simple JWT."""
            refresh = RefreshToken.for_user(user)

            # Getting the access token from refresh token
            access_token = getattr(refresh, "access_token", None)

            # Checking if access token is None or not
            if access_token is None:
                return Response(
                    data={"detail": "Failed to generate access token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update last login timestamp
            if user:
                user.last_login = str(timezone.now())
                user.save(update_fields=["last_login"])

            # Return success response
            return Response(
                data={
                    "refresh_token": str(refresh),
                    "access_token": str(access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            raise ValidationError(
                {"detail": "Somethings is wrong!. Please try again."}
            ) from error
