def parse(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]
