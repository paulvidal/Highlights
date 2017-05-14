from django.contrib import admin
from fb_highlights.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = User.to_list_display()
    list_filter = User.to_list_filter()
    search_fields = User.search_fields()


admin.site.register(User, UserAdmin)
