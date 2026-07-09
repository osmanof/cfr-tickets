import joblib

from features import sent2features

from process import parse_information


def tokenize(text):
    return str(text).split()


def predict_tags(text, model):
    tokens = tokenize(text)
    sent = [(token, "O") for token in tokens]
    features = sent2features(sent)
    tags = model.predict_single(features)
    return list(zip(tokens, tags))


def extract_entities(text, model):
    text = " ".join(["".join([j for j in i if j.isalpha() or j.isdigit()]) for i in text.split()])

    tagged_tokens = predict_tags(text, model)

    result = {
        "FROM": [],
        "TO": [],
        "DATE_FROM": [],
        "DATE_TO": []
    }

    for token, tag in tagged_tokens:
        if tag == "O":
            continue

        entity_type = tag

        if entity_type in result:
            result[entity_type].append(token.lower())

    return parse_information(tagged_tokens)
