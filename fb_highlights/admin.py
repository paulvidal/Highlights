from django.contrib import admin
from fb_highlights.models import User, RegistrationTeam, LatestHighlight, FootballTeam, NewFootballRegistration, \
    HighlightStat, \
    HighlightNotificationStat, RegistrationCompetition, FootballCompetition, ScrappingStatus, ScraperApiKey, \
    BlockedNotification, Recommendation, FootballTeamMapping, FootballCompetitionMapping, HighlightImage


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
    list_display = LatestHighlight.to_list_display() + ['goal_data_formatted']
    list_filter = LatestHighlight.to_list_filter()
    search_fields = LatestHighlight.search_fields()
    ordering = '-time_since_added',

    def goal_data_formatted(self, instance):
        goal_data = sorted(instance.goal_data, key=lambda d: d['elapsed'])
        return '__'.join([str(g['player']) for g in goal_data]).replace(' ', '_')


class FootballTeamAdmin(admin.ModelAdmin):
    list_display = FootballTeam.to_list_display()
    list_filter = FootballTeam.to_list_filter()
    search_fields = FootballTeam.search_fields()


class FootballCompetitionAdmin(admin.ModelAdmin):
    list_display = FootballCompetition.to_list_display()
    list_filter = FootballCompetition.to_list_filter()
    search_fields = FootballCompetition.search_fields()


class NewFootballRegistrationAdmin(admin.ModelAdmin):
    list_display = NewFootballRegistration.to_list_display()
    list_filter = NewFootballRegistration.to_list_filter()
    search_fields = NewFootballRegistration.search_fields()


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


class ScrappingStatusAdmin(admin.ModelAdmin):
    list_display = ScrappingStatus.to_list_display()
    list_filter = ScrappingStatus.to_list_filter()
    search_fields = ScrappingStatus.search_fields()


class ScraperApiKeysAdmin(admin.ModelAdmin):
    list_display = ScraperApiKey.to_list_display()
    list_filter = ScraperApiKey.to_list_filter()
    search_fields = ScraperApiKey.search_fields()


class BlockedNotificationAdmin(admin.ModelAdmin):
    list_display = BlockedNotification.to_list_display()
    list_filter = BlockedNotification.to_list_filter()
    search_fields = BlockedNotification.search_fields()


class RecommendationAdmin(admin.ModelAdmin):
    list_display = Recommendation.to_list_display()
    list_filter = Recommendation.to_list_filter()
    search_fields = Recommendation.search_fields()


class FootballTeamMappingAdmin(admin.ModelAdmin):
    list_display = FootballTeamMapping.to_list_display()
    list_filter = FootballTeamMapping.to_list_filter()
    search_fields = FootballTeamMapping.search_fields()
    ordering = 'team',


class FootballCompetitionMappingAdmin(admin.ModelAdmin):
    list_display = FootballCompetitionMapping.to_list_display()
    list_filter = FootballCompetitionMapping.to_list_filter()
    search_fields = FootballCompetitionMapping.search_fields()
    ordering = 'competition',


class HighlightImageAdmin(admin.ModelAdmin):
    list_display = HighlightImage.to_list_display()
    list_filter = HighlightImage.to_list_filter()
    search_fields = HighlightImage.search_fields()
    ordering = '-match_id',


admin.site.register(User, UserAdmin)
admin.site.register(RegistrationTeam, RegistrationTeamAdmin)
admin.site.register(RegistrationCompetition, RegistrationCompetitionAdmin)
admin.site.register(LatestHighlight, LatestHighlightAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballCompetition, FootballCompetitionAdmin)
admin.site.register(NewFootballRegistration, NewFootballRegistrationAdmin)
admin.site.register(HighlightStat, HighlightStatAdmin)
admin.site.register(HighlightNotificationStat, HighlightNotificationStatAdmin)
admin.site.register(ScrappingStatus, ScrappingStatusAdmin)
admin.site.register(ScraperApiKey, ScraperApiKeysAdmin)
admin.site.register(BlockedNotification, BlockedNotificationAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(FootballTeamMapping, FootballTeamMappingAdmin)
admin.site.register(FootballCompetitionMapping, FootballCompetitionMappingAdmin)
admin.site.register(HighlightImage, HighlightImageAdmin)
