import os

import frappe
from frappe import _


def check_policy_import_permission(dt):
	if dt.doctype == "WMS Insurance Import":
		allowed_roles = ["Insurance Manager", "System Manager", "WMS Administrator"]
		if not any(role in allowed_roles for role in frappe.get_roles(frappe.session.user)):
			frappe.throw(
				_("You are not permitted to perform this action."),
				frappe.PermissionError,
			)


def validate_file_type(file_path, dt):
	if dt.doctype == "WMS Insurance Import":
		if dt.equest_type == "Policy Expiry Register":
			ext = os.path.splitext(file_path)[1].lower()
			if ext not in [".html", ".htm"]:
				frappe.throw(_("Only HTML files are allowed. You uploaded: {0}").format(ext))
