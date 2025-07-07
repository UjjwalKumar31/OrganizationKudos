from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization, Kudo

# Register your models here.

class ReceivedKudoInline(admin.TabularInline):
    """
    Inline admin for displaying Kudos received by a user
    on the User detail page in the Django admin.
    """
    model = Kudo
    fk_name = 'receiver'  # Show kudos received by the user
    extra = 0
    readonly_fields = ('sender', 'message', 'created_at')
    can_delete = False

class SentKudoInline(admin.TabularInline):
    """
    Inline admin for displaying Kudos sent by a user
    on the User detail page in the Django admin.
    """
    model = Kudo
    fk_name = 'sender'  # Show kudos sent by the user
    extra = 0
    readonly_fields = ('receiver', 'message', 'created_at')
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the custom User model.
    Extends Django's default UserAdmin and adds support
    for 'organization' and inline display of Kudos activity.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Organization Info', {'fields': ('organization',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Organization Info', {'fields': ('organization',)}),
    )
    list_display = BaseUserAdmin.list_display + ('organization',)
    list_filter = BaseUserAdmin.list_filter + ('organization',)

    inlines = [SentKudoInline, ReceivedKudoInline]

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Organizations.
    Displays organization ID and name in the list view.
    """
    list_display = ('id', 'name')

@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    """
    Admin interface for managing individual Kudos.
    Displays sender, receiver, message, and timestamp.
    """
    list_display = ('id', 'sender', 'receiver', 'message', 'created_at')
    readonly_fields = ('created_at',)
