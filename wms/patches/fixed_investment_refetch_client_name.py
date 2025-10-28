import frappe


def execute():
	null_client_name_list = frappe.get_all(
		"WMS Fixed Investment", filters={"client_name": None}, fields=["name", "client"]
	)
	[
		frappe.set_value(
			"WMS Fixed Investment",
			item["name"],
			"client_name",
			frappe.get_value("WMS Client", item["client"], "client_name"),
		)
		for item in null_client_name_list
	]
