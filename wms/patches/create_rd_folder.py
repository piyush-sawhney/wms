import frappe


def execute():
	folder_name = "RD Schedules"
	if frappe.db.exists("File", {"file_name": folder_name, "is_folder": 1}):
		return

	folder = frappe.get_doc({
		"doctype": "File",
		"file_name": folder_name,
		"is_folder": 1,
		"folder": "Home"
	})
	folder.insert(ignore_permissions=True)