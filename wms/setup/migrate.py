import frappe

@frappe.whitelist()
def before_migrate():
    frappe.cache.delete_value("assets_json", shared=True)
    frappe.db.commit()

@frappe.whitelist()
def after_migrate():
    frappe.cache.delete_value("assets_json", shared=True)
    frappe.db.commit()