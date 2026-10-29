def discounted(cents, percent):
    if cents < 0 or not 0 <= percent <= 100:
        raise ValueError("out of range")
    return (cents * (100-percent) + 50) // 100
