import frappe


def execute():
	entry_done_status_list = frappe.get_all(
		"WMS PO Investment", filters={"status": "Entry Done"}, fields=["name"]
	)
	for item in entry_done_status_list:
		frappe.set_value("WMS PO Investment", item["name"], "passbook_status", "Not Created")

	submitted_to_po_status_list = frappe.get_all(
		"WMS PO Investment", filters={"status": "Submitted to PO"}, fields=["name"]
	)
	for item in submitted_to_po_status_list:
		frappe.set_value("WMS PO Investment", item["name"], "status", "Submitted")
		frappe.set_value("WMS PO Investment", item["name"], "passbook_status", "Not Created")

	passbook_received_status_list = frappe.get_all(
		"WMS PO Investment", filters={"status": "Passbook Received"}, fields=["name"]
	)
	for item in passbook_received_status_list:
		frappe.set_value("WMS PO Investment", item["name"], "status", "Active")
		frappe.set_value("WMS PO Investment", item["name"], "passbook_status", "With Us")

	passbook_sent_to_customer_status_list = frappe.get_all(
		"WMS PO Investment", filters={"status": "Passbook Sent to Customer"}, fields=["name"]
	)
	for item in passbook_sent_to_customer_status_list:
		frappe.set_value("WMS PO Investment", item["name"], "status", "Active")
		frappe.set_value("WMS PO Investment", item["name"], "passbook_status", "With Client")
