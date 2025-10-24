import os

import frappe

from wms.wms_data_import.doctype.wms_insurance_import.html_file_processor import (
	process_new_india_policy_expiry_register_html,
)
from wms.wms_data_import.helpers.import_validators import (
	validate_file_type,
)


def process_new_india_policy_expiry_register(dt):
	file_path = frappe.get_site_path(dt.upload_file.lstrip("/"))
	validate_file_type(file_path, dt.report_type)
	if not os.path.exists(file_path):
		frappe.throw(f"File not found: {file_path}")
	process_new_india_policy_expiry_register_html(dt, file_path)
