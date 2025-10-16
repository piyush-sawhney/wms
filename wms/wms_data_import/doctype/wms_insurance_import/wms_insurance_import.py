# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
from bs4 import BeautifulSoup
from datetime import datetime
from wms.wms_data_import.doctype.wms_insurance_import.html_file_processor import process_new_india_policy_expiry_register_html
class WMSInsuranceImport(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		error_log: DF.LongText | None
		from_date: DF.Date | None
		insurance_provider: DF.Link | None
		name: DF.Int | None
		report_type: DF.Literal["Premium Register", "Policy Expiry Register"]
		status: DF.Literal["", "Pending", "Processing", "Completed", "Failed"]
		to_date: DF.Date | None
		upload_file: DF.Attach | None
	# end: auto-generated types
	pass


def process_new_india_policy_expiry_register(dt):
	file_path = frappe.get_site_path(dt.upload_file.lstrip("/"))
	if not os.path.exists(file_path):
		frappe.throw(f"File not found: {file_path}")
	process_new_india_policy_expiry_register_html(file_path)
	

@frappe.whitelist()
def import_insurance_policies(docname):
	dt = frappe.get_doc("WMS Insurance Import", docname)
	if dt.insurance_provider and dt.insurance_provider == "The New India Assurance Co Ltd":
		if dt.report_type == "Policy Expiry Register":
			process_new_india_policy_expiry_register(dt)

	# frappe.msgprint(f"Importing insurance policies for document: {dt}")