# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import os
from datetime import datetime

import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.model.document import Document

from wms.wms_data_import.doctype.wms_insurance_import.new_india_processor import (
	process_new_india_policy_expiry_register,
)
from wms.wms_data_import.helpers.import_validators import (
	check_policy_import_permission,
)


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
		success_log: DF.LongText | None
		to_date: DF.Date | None
		upload_file: DF.Attach | None
	# end: auto-generated types
	pass

	def validate(self):
		self.validate_file_type()

	def validate_file_type(self):
		if not self.upload_file:
			frappe.throw(_("Please attach a file before saving."))


@frappe.whitelist()
def import_insurance_policies(docname):
	doctype = "WMS Insurance Import"
	check_policy_import_permission(doctype)
	dt = frappe.get_doc(doctype, docname)
	if dt.insurance_provider and dt.insurance_provider == "The New India Assurance Co Ltd":
		if dt.report_type == "Policy Expiry Register":
			from_date, to_date = process_new_india_policy_expiry_register(dt)
			dt.from_date = from_date
			dt.to_date = to_date
			dt.status = "Completed"
			dt.save(ignore_permissions=True)

	# frappe.msgprint(f"Importing insurance policies for document: {dt}")
