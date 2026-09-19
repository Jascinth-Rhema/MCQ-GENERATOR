def clean_text(text):
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text


def prepare_text(text, max_length=6000):
    text = clean_text(text)

    if len(text) > max_length:
        text = text[:max_length]

    return text