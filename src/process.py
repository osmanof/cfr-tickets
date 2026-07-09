from constants import CITIES, CITIES_FROM, CITIES_TO, MONTHS, WHEN


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


def choose_most_relevant(lst, index):
    result = []
    for i in lst:
        if i[0] <= index + 3:
            result.append(i)
        else:
            return result

    return result


def parse_information(raw_list):
    tags = {
        "FROM": [],
        "TO": [],
        "DATE_FROM": [],
        "DATE_TO": []
    }
    for word, tag in raw_list:
        word = word.lower()

        if tag == "O":
            continue

        for _tag in tags:
            if tag == f"B-{_tag}":
                tags[_tag].append(word)
            elif tag == f"I-{_tag}":
                if len(tags[_tag]):
                    tags[_tag][-1] += " " + word

    return {
        "FROM": get_city_from_raw_text(tags["FROM"], CITIES + CITIES_FROM) if tags["FROM"] else [],
        "TO": get_city_from_raw_text(tags["TO"], CITIES + CITIES_TO) if tags["TO"] else [],
        "DATE_FROM": process_date(tags["DATE_FROM"]) if tags["DATE_FROM"] else [],
        "DATE_TO": process_date(tags["DATE_TO"]) if tags["DATE_TO"] else []
    }


def get_element_containing_number(lst):
    for word in lst:
        for i in word.split():
            if i.isdigit():
                return int(i), word

    return None


def process_date(raw_text):
    raw_text = [word.lower() for word in raw_text]

    words = [get_element_containing_number(raw_text)]

    if words == [None]:
        words = []

        for word in raw_text:
            if word not in PROHIBITED_WORDS:
                words.append((None, word))

    tmp = []
    for number, word in words:
        distances = [(levenshtein_distance(word, month), month, (number, word), index) for index, month in enumerate(MONTHS + WHEN)]

        tmp.append(min(distances, key=lambda x: x[0]))

    tmp.sort(key=lambda x: x[0])
    minimal = tmp[0][0]

    return sorted(choose_most_relevant(tmp, minimal), key=lambda x: len(x[1]), reverse=True)[0]


def get_city_from_raw_text(raw_text, cities_list):
    raw_text = [word.lower() for word in raw_text]

    words = []

    for word in raw_text:
        if word not in PROHIBITED_WORDS:
            words.append(word)

    tmp = []
    for i in words:
        distances = [(levenshtein_distance(i, city), city, index) for index, city in enumerate(cities_list)]

        tmp.append(min(distances, key=lambda x: x[0]))

    tmp.sort(key=lambda x: x[0])
    minimal = tmp[0][0]

    return sorted(choose_most_relevant(tmp, minimal), key=lambda x: len(x[1]), reverse=True)[0]


if __name__ == "__main__":
    print(parse_information(

    [('привет.', 'B-TO'),
     ('мы', 'B-FROM'),
     ('короче', 'O'),
     ('с', 'O'),
     ('семьей', 'B-FROM'),
     ('собрались', 'B-TO'),
     ('НГ', 'B-FROM'),
     ('отметить.', 'B-TO'),
     ('хотим', 'O'),
     ('билет', 'O'),
     ('из', 'O'),
     ('Нижнего', 'B-FROM'),
     ('Тагила', 'I-FROM'),
     ('в', 'O'),
     ('Минеральные', 'B-TO'),
     ('воды', 'I-TO'),
     ('31', 'B-DATE_FROM'),
     ('декабря', 'I-DATE_FROM'),
     ('до', 'O'),
     ('6', 'B-DATE_TO'),
     ('января.', 'I-DATE_TO'),
     ('Все', 'O'),
     ('таки', 'B-FROM'),
     ('отходнуть', 'B-TO'),
     ('тоже', 'B-FROM'),
     ('надо)', 'B-TO'),
     ('на', 'O'),
     ('недельнку', 'B-TO'),
     ('поедем', 'I-TO')]

    ))
