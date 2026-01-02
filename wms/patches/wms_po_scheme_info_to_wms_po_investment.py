import frappe

def execute():
    po_investment_list = frappe.get_all(
        "WMS PO Investment", fields=["name", "scheme_code"]
    )

    for po_investment in po_investment_list:
        scheme_name = frappe.db.get_value(
            "WMS PO Scheme Info",
            {"name": po_investment["scheme_code"]},
            "name"
        )
        if scheme_name:
                frappe.db.set_value(
				"WMS PO Investment",
				po_investment["name"],
				"scheme_name",
				scheme_name,
				update_modified=False
			)

    frappe.db.commit()
    frappe.clear_cache()
