from parser import parse
from scoring import score
def process(text):
    return score(parse(text))
