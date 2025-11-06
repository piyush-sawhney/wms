import frappe


def execute():
	entry_done_status_list = frappe.get_all(
		"WMS Fixed Investment", filters={"status": "Entry Done"}, fields=["name"]
	)
	for item in entry_done_status_list:
		frappe.set_value("WMS Fixed Investment", item["name"], "fd_status", "Not Created")

	submitted_status_list = frappe.get_all(
		"WMS Fixed Investment", filters={"status": "Submitted"}, fields=["name"]
	)
	for item in submitted_status_list:
		frappe.set_value("WMS Fixed Investment", item["name"], "fd_status", "Not Created")
