# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSService(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from wms.wms_core.doctype.wms_service_tracking.wms_service_tracking import WMSServiceTracking

		description: DF.SmallText | None
		entry_date: DF.Date
		service_entity: DF.Link
		service_item: DF.DynamicLink
		status: DF.Literal[
			"Entry Done", "Submitted", "Client Dependency", "Pending With Us", "Resolved", "Rejected"
		]
		tracking_updates: DF.Table[WMSServiceTracking]
		type: DF.Link
	# end: auto-generated types
	pass
