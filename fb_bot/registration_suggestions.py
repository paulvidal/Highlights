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
      "champions league",
      "manchester city",
      "spain",
      "la liga",
    ],

    "bayern munich": [
      "champions league",
      "monaco",
      "germany",
      "bundesliga",
    ],

    "chelsea": [
      "champions league",
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
      "champions league",
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
      "champions league",
      "tottenham",
      "england",
      "premier league",
    ],

    "marseille": [
      "monaco",
      "bordeaux",
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
      "champions league",
      "bayern munich",
      "france",
      "ligue 1",
    ],

    "real madrid": [
      "champions league",
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


def get_default_suggestion_for_registration():
    return get_suggestion_for_registrations([])


def get_suggestion_for_registrations(registrations):
    # shuffle registrations
    random.shuffle(registrations)

    # Suggestion
    suggestions = []

    for r in registrations:
        if SUGGESTIONS.get(r):
            suggestions += SUGGESTIONS.get(r)

    # Add default suggestions
    suggestions += ['psg', 'arsenal', 'champions league', 'barcelona', 'manchester united', 'europa league',
                    'bayern munich', 'real madrid', 'liverpool']

    # Remove teams already in registrations
    suggestions = [s for s in suggestions if s not in registrations]
    # Remove duplicates while keeping order
    suggestions = _remove_duplicates_and_keep_order(suggestions)

    return suggestions[:10]


def _remove_duplicates_and_keep_order(list):
    return sorted(set(list), key=lambda x: list.index(x))
