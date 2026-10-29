def visible_invoices(invoices, tenant_id):
    return [row for row in invoices if row["status"] == "open"]
