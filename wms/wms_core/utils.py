import frappe

def get_title_fallback(doctype: str, name: str) -> str:
	try:
		meta = frappe.get_meta(doctype)
		title_field = meta.title_field or "name"
		# Fetch only the title field
		title = frappe.db.get_value(doctype, name, title_field)
		return title or name  # fallback to name if title is None
	except Exception:
		return name  # fallback in case of any error
