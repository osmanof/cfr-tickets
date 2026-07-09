def word2features(sent, i):
    word = sent[i][0]

    features = {
        "bias": 1.0,
        "word.lower": word.lower(),
        "word": word,
        "word[-1:]": word[-1:],
        "word[-2:]": word[-2:],
        "word[-3:]": word[-3:],
        "word.isupper": word.isupper(),
        "word.istitle": word.istitle(),
        "word.isdigit": word.isdigit(),
        "contains_digit": any(ch.isdigit() for ch in word),
        "contains_hyphen": "-" in word,
    }

    if i > 0:
        prev_word = sent[i - 1][0]
        features.update({
            "-1:word.lower": prev_word.lower(),
            "-1:word": prev_word,
            "-1:word.istitle": prev_word.istitle(),
            "-1:word.isdigit": prev_word.isdigit(),
        })
    else:
        features["BOS"] = True

    if i < len(sent) - 1:
        next_word = sent[i + 1][0]
        features.update({
            "+1:word.lower": next_word.lower(),
            "+1:word": next_word,
            "+1:word.istitle": next_word.istitle(),
            "+1:word.isdigit": next_word.isdigit(),
        })
    else:
        features["EOS"] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, label in sent]
