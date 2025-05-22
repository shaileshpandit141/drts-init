from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import SafeText

from .forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model that extends Django"s built-in UserAdmin.
    Customizes the admin forms, display fields and fieldsets for managing users.
    """

    model = User
    add_form = UserCreationForm  # Custom form for creating new users
    form = UserChangeForm  # Custom form for modifying existing users

    # Fields to display in the user list view
    list_display = [
        field.name
        for field in User._meta.get_fields()
        if not (field.many_to_many or field.one_to_many or field.name == "password")
    ]
    list_display_links = list_display
    list_filter = ["is_staff", "is_superuser", "is_active", "is_verified", "last_login"]
    search_fields = ["email", "username", "first_name", "last_name"]
    readonly_fields = ["date_joined", "last_login"]
    ordering = ("-last_login",)
    list_per_page = 16

    def full_name(self, obj) -> str:
        """Get full name of user"""
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"  # type: ignore

    def is_active_colored(self, obj) -> SafeText:
        """Get colored active status"""
        if obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        return format_html('<span style="color: red;">Inactive</span>')

    is_active_colored.short_description = "Status"  # type: ignore

    # Define how fields are grouped and displayed when editing existing users
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
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
                    "username",
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

    # Default ordering by newest first
    ordering = ("-date_joined",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    actions = ["activate_users", "deactivate_users", "send_email_verification"]

    def activate_users(self, request, queryset) -> None:
        """Activate selected users"""
        queryset.update(is_active=True)

    activate_users.short_description = "Activate selected users"  # type: ignore

    def deactivate_users(self, request, queryset) -> None:
        """Deactivate selected users"""
        queryset.update(is_active=False)

    deactivate_users.short_description = "Deactivate selected users"  # type: ignore

    def send_email_verification(self, request, queryset) -> None:
        """Send verification emails"""
        for user in queryset:
            # Add your email verification logic here
            pass

    send_email_verification.short_description = "Send email verification"  # type: ignore


# Register the custom admin interface
admin.site.register(User, CustomUserAdmin)
