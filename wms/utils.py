import frappe

def calculate_age(dob):
	dob_date = frappe.utils.getdate(dob)
	today = frappe.utils.nowdate()
	return frappe.utils.date_diff(today, dob_date) // 365

def get_title_fallback(doctype: str, name: str) -> str:
	try:
		meta = frappe.get_meta(doctype)
		title_field = meta.title_field or "name"
		# Fetch only the title field
		title = frappe.db.get_value(doctype, name, title_field)
		return title or name  # fallback to name if title is None
	except Exception:
		return name  # fallback in case of any error
	
def get_financial_year_code(date):
    """Returns financial year code as 'YYYY-YY' e.g., '2025-26' for FY 2025-26"""
    if isinstance(date, str):
        date = frappe.utils.getdate(date)

    start_year = date.year
    if date.month < 4:
        start_year -= 1

    end_year = (start_year + 1) % 100  # Just get last 2 digits
    return f"{start_year}-{end_year:02d}"