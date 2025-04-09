from django.contrib import admin
from .models import Word, UserSessionData, UserApiMode,UserApiPlan,UserIdentity, OfflineCoaching


@admin.register(Word)
class WordModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'word_name', 'hindi_meaning', 'definition', 'image']


@admin.register(UserSessionData)
class UserSessionDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'data', 'updated_at']


@admin.register(UserApiMode)
class UserApiModeAdmin(admin.ModelAdmin):
    list_display = ['user', 'api_mode']

@admin.register(UserApiPlan)
class UserApiPlanAdmin(admin.ModelAdmin):
    list_display =  ['user', 'duration_in_days', 'activating_time']


@admin.register(UserIdentity)
class UserIdentityAdmin(admin.ModelAdmin):
    list_display = ['user', 'identity']






@admin.register(OfflineCoaching)
class OfflineCoachingAdmin(admin.ModelAdmin):
    list_display = ['user', 'coaching_institute_name', 'city', 'contact_number', 'status', 'created_at', 'updated_at']