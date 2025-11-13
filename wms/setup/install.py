import frappe


# After Install Hook
def after_install():
	update_app_name()
	update_backup_setting()
	create_folders()

def create_folders():
	folder = frappe.get_doc({
        "doctype": "File",
        "file_name": "RD Schedules",
        "is_folder": 1,
        "folder": "Home"
    })
	folder.insert(ignore_permissions=True)


def update_app_name():
	frappe.db.set_value("System Settings", None, "default_app", "wms")
	frappe.db.set_value("Website Settings", None, "app_name", "KNAPS Financial Services")
	frappe.db.set_value("Website Settings", None, "title_prefix", "KNAPS Financial Services")


def update_backup_setting():
	frappe.db.set_value("System Settings", None, "encrypt_backup", 1)
	frappe.db.set_value("System Settings", None, "backup_limit", 10)


# Before Uninstall Hook
def before_uninstall():
	frappe.db.set_value("System Settings", None, "default_app", "")
	frappe.db.set_value("System Settings", None, "encrypt_backup", 0)
	frappe.db.set_value("System Settings", None, "backup_limit", 3)
