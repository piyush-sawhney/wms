# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSNominee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		dob: DF.Data | None
		guardian_dob: DF.Date | None
		guardian_name: DF.Link | None
		guardian_relation: DF.Link | None
		is_minor: DF.Check
		nominee_name: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		relation: DF.Link
		share_percent: DF.Percent
	# end: auto-generated types
	pass
