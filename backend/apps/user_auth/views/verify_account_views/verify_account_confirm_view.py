from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.user_auth.throttles import AuthUserRateThrottle
from limited_time_token_handler import LimitedTimeTokenDecoder, TokenError
from rest_core.response import failure_response, success_response

User = get_user_model()


class VerifyAccountConfirmView(APIView):
    """API View for verifying user accounts via email confirmation."""

    throttle_classes = [AuthUserRateThrottle]

    def get(self, request) -> Response:
        token = request.query_params.get("token")
        return self._verify_token(token)

    def post(self, request) -> Response:
        token = request.data.get("token")
        return self._verify_token(token)

    def _verify_token(self, token: str) -> Response:
        if not token:
            return failure_response(
                message="Token is missing",
                errors={
                    "token": [
                        "Token field is required. Please provide a valid verification token."
                    ]
                },
            )

        try:
            decoder = LimitedTimeTokenDecoder(token)
            if not decoder.is_valid():
                raise TokenError("The verification token is invalid or has expired.")

            data = decoder.decode()
            user = User.objects.get(id=data.get("user_id"))

            if getattr(user, "is_verified", False):
                return success_response(
                    message="Account Already Verified",
                    data={"detail": "This account has already been verified."},
                )

            setattr(user, "is_verified", True)
            user.save()

            return success_response(
                message="Account verification successful",
                data={"detail": "Your account has been verified successfully."},
            )

        except User.DoesNotExist:
            return failure_response(
                message="Invalid verification token",
                errors={"token": ["The token is valid but the user does not exist."]},
            )

        except TokenError:
            return failure_response(
                message="Invalid verification token",
                errors={
                    "token": [
                        "The provided verification token is invalid or has expired."
                    ]
                },
            )
