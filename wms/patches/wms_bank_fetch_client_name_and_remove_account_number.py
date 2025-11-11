import frappe


def execute():
	# Update client_name in WMS Bank from linked WMS Client
	null_client_name_list = frappe.get_all(
		"WMS Bank", filters={"client_name": None}, fields=["name", "client"]
	)
	[
		frappe.set_value(
			"WMS Bank",
			item["name"],
			"client_name",
			frappe.get_value("WMS Client", item["client"], "client_name"),
		)
		for item in null_client_name_list
	]
	# Truncate account_number to last 4 digits for non-Post Office banks
	non_post_office_banks = frappe.get_all(
		"WMS Bank", filters={"bank_name": ["not like", "%post office%"]}, pluck="name"
	)

	for bank_name in non_post_office_banks:
		bank_doc = frappe.get_doc("WMS Bank", bank_name)
		if bank_doc.account_number and len(bank_doc.account_number) > 4:
			bank_doc.account_number = bank_doc.account_number[-4:]
			bank_doc.save(ignore_permissions=True)

	# Remove Account Number from Payment
	payment_list = frappe.get_all("WMS Payment")
	for payment_name in payment_list:
		payment_doc = frappe.get_doc("WMS Payment", payment_name)
		bank_doc = frappe.get_doc("WMS Bank", payment_doc.bank, pluck="bank_name")
		if "post office" not in bank_doc.bank_name.lower():
			payment_doc.account_number = payment_doc.account_number[-4:]
			payment_doc.save(ignore_permissions=True)
