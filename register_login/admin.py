from django.contrib import admin

from .models import AccountEmailConfirmation


@admin.register(AccountEmailConfirmation)
class AccountEmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'acceptance')
    list_filter = ('acceptance',)
