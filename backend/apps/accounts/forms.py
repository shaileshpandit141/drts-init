from typing import cast

from django import forms
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.validators import validate_email
from django.forms import ValidationError

from .models import User


class UserCreationForm(DjangoUserCreationForm):  # type: ignore  # noqa: PGH003
    """A form for creating new users. Extends Django's built-in UserCreationForm."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Your password must contain at least 8 characters.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Enter the same password as above, for verification.",
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=False
    )
    is_active = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    class Meta(DjangoUserCreationForm.Meta):  # type: ignore  # noqa: PGH003
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "picture",
            "is_active",
            "is_verified",
            "is_staff",
        )

    def clean_email(self) -> str:
        """Custom validation for email field."""
        email = self.cleaned_data.get("email")
        if not email:
            msg: str = "Email is required."
            raise ValidationError(msg)

        try:
            validate_email(email)
        except ValidationError as error:
            msg = "Please enter a valid email address."
            raise ValidationError(msg) from error

        if User.objects.filter(email=email.lower()).exists():
            msg = "A user with this email already exists."
            raise ValidationError(msg)

        return email.lower()

    def clean_password2(self) -> str:
        """Verify that both passwords match and meet minimum requirements."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise ValidationError(msg)

        if not password1:
            msg = "Password is required"
            raise ValidationError(msg)

        if len(password1) < 8:  # noqa: PLR2004
            msg = "Password must be at least 8 characters long"
            raise ValidationError(msg)

        if password2 is None:
            return ""

        return password2

    def save(self, commit: bool = True) -> User:  # noqa: FBT001, FBT002
        user = cast("User", super().save(commit=False))
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):  # type: ignore  # noqa: PGH003
    """A form for updating users. Extends Django's built-in UserChangeForm."""

    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control", "style": "margin-block: 8px;"}
        ),
    )
    is_active = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    class Meta(DjangoUserChangeForm.Meta):  # type: ignore  # noqa: PGH003
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "picture",
            "is_active",
            "is_verified",
            "is_staff",
        )

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        user = cast("User", self.instance)  # type: ignore  # noqa: PGH003
        if user and user.picture:
            self.fields[
                "picture"
            ].help_text = f'<a href="{user.picture.url}" target="_blank" style="padding-inline: 4px;">View Current picture</a>'

    def clean_email(self) -> str:
        """Validation for email field."""
        email = self.cleaned_data.get("email")
        if not email:
            msg = "Email is required."
            raise ValidationError(msg)

        try:
            validate_email(email)
        except ValidationError as error:
            msg = "Please enter a valid email address."
            raise ValidationError(msg) from error

        return email.lower()

    def save(self, commit: bool = True) -> User:  # noqa: FBT001, FBT002
        user = cast("User", super().save(commit=False))
        if commit:
            user.save()
        return user
