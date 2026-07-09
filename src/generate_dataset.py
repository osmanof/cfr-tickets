import csv
import random

from src.constants import *

from constants import TEMPLATES, MONTHS


dates = [
    "завтра",
    "послезавтра",
    "в субботу",
    "на выходных",
    "понедельник",
    "вторник",
    "среду",
    "четверг",
    "пятницу",
    "субботу",
    "воскресенье"
]

for month in MONTHS:
    for i in range(1, 29):
        dates.append(f"{i} {month}")


fillers_start = [
    "привет найди пожалуйста билет",
    "здравствуйте мне нужен билет",
    "мне срочно нужно улететь",
    "хочу слетать",
    "подскажи плиз билеты",
    "ку еду",
    "приветик ищу билеты",
    "салам посмотри рейсы",
    "привет в общем нужен билет на",
    "можно мне билет",
    "дай пожалуйста билет",
    "хочется полетать",
    "к родственникам лечу нужен",
    "билет",
    "самолет",
    "нужен билет"
]


fillers_end = [
    "где-то",
    "срочно",
    "подешевле",
    "прямой рейс",
    "плиз",
    "акции есть",
    "примерно",
    "пж",
    "спасибо"
]


def make_city_variant(city):
    variants = []

    variants.append(city)

    if "-" in city:
        variants.append(city.replace("-", " "))

    variants.append(city.lower())

    if "-" in city:
        variants.append(city.replace("-", " ").lower())

    return random.choice(variants)


def add_entity(words, tags, entity_text, entity_type):
    entity_words = entity_text.split()

    for i, word in enumerate(entity_words):
        words.append(word)

        if i == 0:
            tags.append(f"B-{entity_type}")
        else:
            tags.append(f"I-{entity_type}")


def add_o_text(words, tags, text):
    for word in text.split():
        words.append(word)
        tags.append("O")


def generate_csv_dataset(filename="../data/sentences.csv", num_samples=20000):
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "tags"])

        for _ in range(num_samples):
            template = random.choice(TEMPLATES)

            base_from = random.choice(CITIES_FROM)
            base_to = random.choice(CITIES_TO)

            while base_to == base_from:
                base_to = random.choice(CITIES_TO)

            c_from = make_city_variant(base_from)
            c_to = make_city_variant(base_to)

            date_to = random.choice(dates)
            date_from = random.choice(dates)

            words = []
            tags = []

            if random.random() > 0.4:
                add_o_text(words, tags, random.choice(fillers_start))

            for part in template.split():
                if part == "FROM":
                    add_entity(words, tags, c_from, "FROM")

                elif part == "TO":
                    add_entity(words, tags, c_to, "TO")

                elif part == "DATE_FROM":
                    add_entity(words, tags, date_from, "DATE_FROM")

                elif part == "DATE_TO":
                    add_entity(words, tags, date_to, "DATE_TO")

                else:
                    words.append(part)
                    tags.append("O")

            if random.random() > 0.4:
                add_o_text(words, tags, random.choice(fillers_end))

            if len(words) != len(tags):
                raise ValueError(
                    f"Ошибка генерации:\n"
                    f"words = {words}\n"
                    f"tags = {tags}\n"
                    f"len(words) = {len(words)}, len(tags) = {len(tags)}"
                )

            writer.writerow([" ".join(words), " ".join(tags)])


generate_csv_dataset(num_samples=150000)