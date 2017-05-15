from django.contrib import admin
from fb_highlights.models import User, Team, LatestHighlight


class UserAdmin(admin.ModelAdmin):
    list_display = User.to_list_display()
    list_filter = User.to_list_filter()
    search_fields = User.search_fields()


class TeamAdmin(admin.ModelAdmin):
    list_display = Team.to_list_display()
    list_filter = Team.to_list_filter()
    search_fields = Team.search_fields()


class LatestHighlightAdmin(admin.ModelAdmin):
    list_display = LatestHighlight.to_list_display()
    list_filter = LatestHighlight.to_list_filter()
    search_fields = LatestHighlight.search_fields()


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(LatestHighlight, LatestHighlightAdmin)
