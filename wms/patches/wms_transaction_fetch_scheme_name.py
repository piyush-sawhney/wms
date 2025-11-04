import frappe


def execute():
	null_scheme_name_list = frappe.get_all(
		"WMS MF Transaction", filters={"scheme_name": None}, fields=["name", "scheme"]
	)
	[
		frappe.set_value(
			"WMS MF Transaction",
			item["name"],
			"scheme_name",
			frappe.get_value("WMS MF Scheme", item["scheme"], "scheme_name"),
		)
		for item in null_scheme_name_list
	]
