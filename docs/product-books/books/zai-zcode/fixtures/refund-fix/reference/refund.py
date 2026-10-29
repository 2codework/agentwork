def refund(balance_cents, requested_cents):
    if type(balance_cents) is not int or type(requested_cents) is not int:
        raise ValueError("integer cents required")
    if balance_cents < 0 or requested_cents < 0 or requested_cents > balance_cents:
        raise ValueError("invalid amount")
    return balance_cents - requested_cents
