def payable(cents):
    return cents - 1000 if cents > 10000 else cents
