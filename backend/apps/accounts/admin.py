from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString

from .forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):  # type: ignore  # noqa: PGH003
    """Custom admin interface for User model."""

    model = User
    add_form = UserCreationForm  # Custom form for creating new users
    form = UserChangeForm  # Custom form for modifying existing users

    # Fields to display in the user list view
    list_display = [  # noqa: RUF012
        "id",
        "email",
        "is_active",
        "is_verified",
        "is_staff",
        "is_superuser",
        "last_login",
    ]
    list_display_links = list_display  # type: ignore  # noqa: PGH003
    list_filter = [  # noqa: RUF012
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
    ]
    search_fields = [  # noqa: RUF012
        "email",
        "first_name",
        "last_name",
    ]
    readonly_fields = [  # noqa: RUF012
        "date_joined",
        "last_login",
    ]
    ordering = ("-last_login",)
    list_per_page = 16

    def full_name(self, obj: User) -> str:
        """Get full name of user."""
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"  # type: ignore  # noqa: PGH003

    def is_active_colored(self, obj: User) -> SafeString:
        """Get colored active status."""
        if obj.is_active:
            return format_html('<span style="color: green;">{}</span>', "Active")
        return format_html('<span style="color: red;">{}</span>', "Inactive")

    is_active_colored.short_description = "Status"  # type: ignore  # noqa: PGH003

    # Define how fields are grouped and displayed when editing existing users
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Define fields shown when adding new users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "picture",
                    "is_active",
                    "is_verified",
                    "is_staff",
                ),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    actions = [  # noqa: RUF012
        "activate_users",
        "deactivate_users",
        "send_email_verification",
    ]

    def activate_users(
        self,
        request: HttpRequest,  # noqa: ARG002
        queryset: QuerySet[User],
    ) -> None:
        """Activate selected users."""
        queryset.update(is_active=True)

    activate_users.short_description = "Activate selected users"  # type: ignore  # noqa: PGH003

    def deactivate_users(
        self,
        request: HttpRequest,  # noqa: ARG002
        queryset: QuerySet[User],
    ) -> None:
        """Deactivate selected users."""
        queryset.update(is_active=False)

    deactivate_users.short_description = "Deactivate selected users"  # type: ignore  # noqa: PGH003

    def send_email_verification(
        self,
        request: HttpRequest,  # noqa: ARG002
        queryset: QuerySet[User],
    ) -> None:
        """Send verification emails."""
        # Add your email verification logic here
        for _user in queryset:
            pass

    send_email_verification.short_description = "Send email verification"  # type: ignore  # noqa: PGH003


# Register the custom admin interface
admin.site.register(User, CustomUserAdmin)  # type: ignore  # noqa: PGH003
