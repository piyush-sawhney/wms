import frappe


def execute():
	null_client_name_list = frappe.get_all(
		"WMS Insurance Policy", filters={"client_name": None}, fields=["name", "client"]
	)
	[
		frappe.set_value(
			"WMS Insurance Policy",
			item["name"],
			"client_name",
			frappe.get_value("WMS Client", item["client"], "client_name"),
		)
		for item in null_client_name_list
	]
	null_proposer_name_list = frappe.get_all(
		"WMS Insurance Policy", filters={"proposer_name": None}, fields=["name", "proposer"]
	)
	[
		frappe.set_value(
			"WMS Insurance Policy",
			item["name"],
			"proposer_name",
			frappe.get_value("WMS Client", item["proposer"], "proposer_name"),
		)
		for item in null_proposer_name_list
	]
