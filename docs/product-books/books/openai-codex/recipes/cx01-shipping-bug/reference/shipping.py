def fee(subtotal_cents, remote=False):
    if subtotal_cents < 0:
        raise ValueError("negative subtotal")
    base = 0 if subtotal_cents >= 5000 else 500
    return base + (800 if remote else 0)
