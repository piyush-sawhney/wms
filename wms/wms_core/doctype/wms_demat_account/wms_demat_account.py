# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSDematAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		client: DF.Link
		client_id: DF.Data
		company_name: DF.Link
		dp_id: DF.Data
		dp_type: DF.Literal["CDSL", "NSDL"]
		status: DF.Literal["Opening Request", "Opened", "Request with DP", "Client Dependency"]
		trading_id: DF.Data | None
	# end: auto-generated types
	pass
