import frappe
def after_install():
    update_app_name()
    update_backup_setting()

def update_app_name():
    frappe.db.set_value("System Settings", None, "default_app", "wms")

def update_backup_setting():
    frappe.db.set_value("System Settings", None, "encrypt_backup", 1)
    frappe.db.set_value("System Settings", None, "backup_limit", 10)

def before_uninstall():
    frappe.db.set_value("System Settings", None, "default_app", "")
    frappe.db.set_value("System Settings", None, "encrypt_backup", 0)
    frappe.db.set_value("System Settings", None, "backup_limit", 3)
