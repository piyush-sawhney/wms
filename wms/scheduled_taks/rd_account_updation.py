import frappe
def update_po_investment_in_rd_account():
    null_po_investment_rd_account_list = frappe.get_all(
        'WMS RD Account',
        filters={"po_investment": None},
        pluck='name'
    )
    for rd_account in null_po_investment_rd_account_list:
        po_investment = frappe.db.get_value(
            'WMS PO Investment',
            filters={'account_number': rd_account, 'scheme_code': 'RD'},
            pluck='name'
        )
        rd_account_doc = frappe.get_doc('WMS RD Account', rd_account)
        rd_account_doc.po_investment = po_investment
        rd_account_doc.save()
