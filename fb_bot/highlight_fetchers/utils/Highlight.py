import abc
import dateparser

from datetime import datetime


class Highlight:
    __metaclass__ = abc.ABCMeta

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added, goal_data, type):
        self.link = self.form_link(link)
        self.img_link = img_link
        self.view_count = view_count
        self.category = category.lower()

        # Make sure date is always parsed
        if not isinstance(time_since_added, datetime):
            time_since_added = dateparser.parse(time_since_added)

        self.time_since_added = time_since_added

        # Match information
        team1, score1, team2, score2 = self.get_match_info(match_name)

        # Run mapping for football team names as team can be named differently
        self.team1 = team1.lower()
        self.team2 = team2.lower()

        self.score1 = score1
        self.score2 = score2

        # Source of the highlight (website)
        self.source = self.get_source()

        # Type of the video (short, normal, extended)
        self.type = type

        # Goal information
        self.goal_data = goal_data

    @abc.abstractmethod
    def get_match_info(self, match):
        """ Override method """

    @abc.abstractmethod
    def get_source(self):
        """ Override method """

    def swap_home_side(self):
        temp_team = self.team1
        temp_score = self.score1

        self.team1 = self.team2
        self.team2 = temp_team

        self.score1 = self.score2
        self.score2 = temp_score

    def form_link(self, link):
        if 'youtube' in link:
            return link

        # Add only resource link, clear all arguments (to prevent duplicate links)
        return link.split('?')[0] if '?' in link else link

    def get_parsed_time_since_added(self):
        return self.time_since_added

    def __str__(self):
        return str((self.link, self.team1, self.score1, self.team2, self.score2, self.img_link, self.view_count,
                    self.category, self.time_since_added, self.source, self.type, self.goal_data))