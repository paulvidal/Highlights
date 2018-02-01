from django.contrib import admin
from fb_highlights.models import User, Team, LatestHighlight, FootballTeam, NewFootballTeam, HighlightStat, \
    HighlightNotificationStat


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
    ordering = '-time_since_added',


class FootballTeamAdmin(admin.ModelAdmin):
    list_display = FootballTeam.to_list_display()
    list_filter = FootballTeam.to_list_filter()
    search_fields = FootballTeam.search_fields()


class NewFootballTeamAdmin(admin.ModelAdmin):
    list_display = NewFootballTeam.to_list_display()
    list_filter = NewFootballTeam.to_list_filter()
    search_fields = NewFootballTeam.search_fields()


class HighlightStatAdmin(admin.ModelAdmin):
    list_display = HighlightStat.to_list_display()
    list_filter = HighlightStat.to_list_filter()
    search_fields = HighlightStat.search_fields()
    ordering = '-time',


class HighlightNotificationStatAdmin(admin.ModelAdmin):
    list_display = HighlightNotificationStat.to_list_display()
    list_filter = HighlightNotificationStat.to_list_filter()
    search_fields = HighlightNotificationStat.search_fields()
    ordering = '-send_time',


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(LatestHighlight, LatestHighlightAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(NewFootballTeam, NewFootballTeamAdmin)
admin.site.register(HighlightStat, HighlightStatAdmin)
admin.site.register(HighlightNotificationStat, HighlightNotificationStatAdmin)
