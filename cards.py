import random


CARDS = [
    {
        "id": 1,
        "character": "Лим Джугён",
        "drama": "Истинная красота",
        "rarity": "⭐⭐⭐",
    },
    {
        "id": 2,
        "character": "Ли Сухо",
        "drama": "Истинная красота",
        "rarity": "⭐⭐⭐⭐",
    },
    {
        "id": 3,
        "character": "Хан Соджун",
        "drama": "Истинная красота",
        "rarity": "⭐⭐⭐⭐",
    },
    {
        "id": 4,
        "character": "Кан Суджин",
        "drama": "Истинная красота",
        "rarity": "⭐⭐⭐",
    },
    {
        "id": 5,
        "character": "Лим Хигён",
        "drama": "Истинная красота",
        "rarity": "⭐⭐",
    },
]


def get_random_card():
    return random.choice(CARDS)
