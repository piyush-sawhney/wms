import frappe


def log_success(dt, message, commit=False):
	"""Append a success message to the document."""
	dt.success_log = (dt.success_log or "") + f"\n{message}"
	if commit:
		dt.save(ignore_permissions=True)
		frappe.db.commit()


def log_error(dt, message, commit=False):
	"""Append an error message to the document."""
	dt.error_log = (dt.error_log or "") + f"\n{message}"
	if commit:
		dt.save(ignore_permissions=True)
		frappe.db.commit()


def bulk_update_logs(dt, success_entries, error_entries, commit=True):
	"""Update logs in bulk (for batch imports)."""
	if success_entries:
		dt.success_log = (dt.success_log or "") + "\n".join(success_entries)
	if error_entries:
		dt.error_log = (dt.error_log or "") + "\n".join(error_entries)
	if commit:
		dt.save(ignore_permissions=True)
		frappe.db.commit()
