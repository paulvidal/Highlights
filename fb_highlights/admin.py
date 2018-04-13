from django.contrib import admin
from fb_highlights.models import User, RegistrationTeam, LatestHighlight, FootballTeam, NewFootballTeam, HighlightStat, \
    HighlightNotificationStat, RegistrationCompetition, NewFootballCompetition, FootballCompetition


class UserAdmin(admin.ModelAdmin):
    list_display = User.to_list_display()
    list_filter = User.to_list_filter()
    search_fields = User.search_fields()
    ordering = '-join_date',


class RegistrationTeamAdmin(admin.ModelAdmin):
    list_display = RegistrationTeam.to_list_display()
    list_filter = RegistrationTeam.to_list_filter()
    search_fields = RegistrationTeam.search_fields()


class RegistrationCompetitionAdmin(admin.ModelAdmin):
    list_display = RegistrationCompetition.to_list_display()
    list_filter = RegistrationCompetition.to_list_filter()
    search_fields = RegistrationCompetition.search_fields()


class LatestHighlightAdmin(admin.ModelAdmin):
    list_display = LatestHighlight.to_list_display()
    list_filter = LatestHighlight.to_list_filter()
    search_fields = LatestHighlight.search_fields()
    ordering = '-time_since_added',


class FootballTeamAdmin(admin.ModelAdmin):
    list_display = FootballTeam.to_list_display()
    list_filter = FootballTeam.to_list_filter()
    search_fields = FootballTeam.search_fields()


class FootballCompetitionAdmin(admin.ModelAdmin):
    list_display = FootballCompetition.to_list_display()
    list_filter = FootballCompetition.to_list_filter()
    search_fields = FootballCompetition.search_fields()


class NewFootballTeamAdmin(admin.ModelAdmin):
    list_display = NewFootballTeam.to_list_display()
    list_filter = NewFootballTeam.to_list_filter()
    search_fields = NewFootballTeam.search_fields()


class NewFootballCompetitionAdmin(admin.ModelAdmin):
    list_display = NewFootballCompetition.to_list_display()
    list_filter = NewFootballCompetition.to_list_filter()
    search_fields = NewFootballCompetition.search_fields()


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
admin.site.register(RegistrationTeam, RegistrationTeamAdmin)
admin.site.register(RegistrationCompetition, RegistrationCompetitionAdmin)
admin.site.register(LatestHighlight, LatestHighlightAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballCompetition, FootballCompetitionAdmin)
admin.site.register(NewFootballTeam, NewFootballTeamAdmin)
admin.site.register(NewFootballCompetition, NewFootballCompetitionAdmin)
admin.site.register(HighlightStat, HighlightStatAdmin)
admin.site.register(HighlightNotificationStat, HighlightNotificationStatAdmin)
