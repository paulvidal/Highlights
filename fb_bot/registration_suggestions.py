import random

SUGGESTIONS = {
    "ac milan": [
      "juventus",
      "italy",
      "serie a",
    ],

    "arsenal": [
      "manchester city",
      "england",
      "premier league",
    ],

    "atletico madrid": [
      "benfica",
      "spain",
      "la liga",
    ],

    "barcelona": [
      "manchester city",
      "spain",
      "la liga",
    ],

    "bayern munich": [
      "monaco",
      "germany",
      "bundesliga",
    ],

    "chelsea": [
      "tottenham",
      "england",
      "premier league",
    ],

    "dortmund": [
      "juventus",
      "germany",
      "bundesliga",
    ],

    "france": [
      "belgium",
      "germany",
      "world cup",
    ],

    "juventus": [
      "dortmund",
      "italy",
      "serie a",
    ],

    "liverpool": [
      "tottenham",
      "england",
      "premier league",
    ],

    "lyon": [
      "bayern munich",
      "france",
      "ligue 1",
    ],

    "manchester city": [
      "barcelona",
      "england",
      "premier league",
    ],

    "manchester united": [
      "tottenham",
      "england",
      "premier league",
    ],

    "marseille": [
      "monaco",
      "bordeau",
      "france",
      "ligue 1",
    ],

    "monaco": [
      "bayern munich",
      "manchester city",
      "france",
    ],

    "montpellier": [
      "monaco",
      "marseille",
      "france",
    ],

    "nantes": [
      "monaco",
      "france",
      "real madrid",
    ],

    "nice": [
      "lyon",
      "france",
      "ligue 1",
    ],

    "paris saint germain": [
      "bayern munich",
      "france",
      "ligue 1",
    ],

    "real madrid": [
      "barcelona",
      "spain",
      "la liga",
    ],

    "tottenham": [
      "manchester city",
      "england",
      "premier league"
    ],
}


def get_suggestion_for_registrations(registrations):
    # shuffle registrations
    random.shuffle(registrations)

    # Suggestion
    suggestions = []

    for r in registrations:
        if SUGGESTIONS.get(r):
            suggestions += SUGGESTIONS.get(r)

    suggestions += ['PSG', 'Barcelona', 'Champions league']

    return suggestions
