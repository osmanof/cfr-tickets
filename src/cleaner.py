from constants import CITIES, CITIES_FROM, CITIES_TO, MONTHS, WHEN


def f(t):
    return t


PROHIBITED_WORDS = [
    "я", "ты", "он", "она", "билет", "пожалуйста", "пж", "спс", "спасибо",
    "хорошо", "они", "самолёт", "самолет", "поезд", "можно", "нужно", "красивый",
    "достопримечательность", "достопримечательности", "неделя", "недели", "неделю",
    "месяц", "месяца", "месяцев", "дети", "детей", "взрослый", "взрослые", "ребенок",
    "ребёнок", "если", "бы", "было", "быть", "только", "важно", "самый", "дешевый",
    "дешёвый", "год", "года", "лет", "пару", "недолго", "отправиться", "отправится",
    "хочу", "хочет", "хотим", "хотят"
]


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def process(lst, index):
    result = []
    for i in lst:
        if i[0] <= index + 2:
            result.append(i)
        else:
            return result

    return result


def process_city(text):
    text = text.lower().split()

    words = []

    for word in text:
        if word not in PROHIBITED_WORDS:
            words.append(word)

    tmp = []
    for i in words:
        u = [(levenshtein_distance(i, city), city, index) for index, city in enumerate(CITIES)]

        tmp.append(min(u, key=lambda x: x[0]))

    tmp.sort(key=lambda x: x[0])
    minimal = tmp[0][0]

    return sorted(process(tmp, minimal), key=lambda x: len(x[1]), reverse=True)[0]


def process_date(text):
    text = text.lower().split()

    words = []
    number = None

    for word in text:
        if word not in PROHIBITED_WORDS:
            words.append(word)
        if word.isdigit():
            number = int(word)

    tmp = []

    if number:
        date_words = MONTHS
    else:
        date_words = MONTHS + WHEN

    for i in words:
        u = [(levenshtein_distance(i, month), month, index) for index, month in enumerate(date_words)]

        tmp.append(min(u, key=lambda x: x[0]))

    tmp.sort(key=lambda x: x[0])
    minimal = tmp[0][0]

    return number, sorted(process(tmp, minimal), key=lambda x: len(x[1]), reverse=True)[0]

