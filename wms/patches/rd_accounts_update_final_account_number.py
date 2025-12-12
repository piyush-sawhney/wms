import frappe


def execute():
	rd_account_list = frappe.get_all("WMS RD Account")
	for rd_account in rd_account_list:
		frappe.get_doc("WMS RD Account", rd_account).save(ignore_permissions=True)
