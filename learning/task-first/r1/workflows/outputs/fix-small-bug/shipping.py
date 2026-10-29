def shipping_fee(order_cents):
    """订单金额为非负整数分；满5000分免运费，否则收600分。"""
    if order_cents >= 5000:
        return 0
    return 600
