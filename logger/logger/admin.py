from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Log

# Change Site Header 
admin.site.site_header = "Logger"

# Unregister Groups
admin.site.unregister(Group)

# Mixin User and Pofile
class ProfileInline(admin.StackedInline):
    model = Profile     



# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


class LogAdmin(admin.ModelAdmin):
    # list_display  = ('body', 'created_at', )
    list_filter = ('created_at', )
    search_fields = ('body', )
    # prepopulated_fields = {'slug': ('title', )}
    # ordering = ['date', 'id']


# Unregister Default User
admin.site.unregister(User)

# Register Custom User, Profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)


# # Register Logs
admin.site.register(Log, LogAdmin)