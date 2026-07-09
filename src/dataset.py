import pandas as pd

df = pd.read_csv("../data/sentences.csv")

df.head()

def tokenize(text):
    return str(text).split()


def row_to_sentence(row):
    tokens = tokenize(row["text"])
    tags = str(row["tags"]).split()

    if len(tokens) != len(tags):
        raise ValueError(
            f"Ошибка несовпадения количества токенов и тегов\n\n"
            f"text: {row['text']}\n"
            f"tokens: {tokens}\n"
            f"tags: {tags}\n"
            f"len(tokens) = {len(tokens)}\n"
            f"len(tags) = {len(tags)}"
        )

    return list(zip(tokens, tags))


def load_sentences(path):
    df = pd.read_csv(path)
    sentences = [row_to_sentence(row) for _, row in df.iterrows()]
    return sentences
