# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class WMSClientGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_group_client.wms_group_client import WMSGroupClient

		clients: DF.Table[WMSGroupClient]
		group_name: DF.Data | None
	# end: auto-generated types
	
	def validate(self):
		self.validate_unique_clients()

	def validate_unique_clients(self):
		unique = set()
		unique_rows = set()
		duplicates = set()
		for row in self.clients:
			if row.client in unique:
				duplicates.add(row.client)

			else:
				unique_rows.add(row)
				unique.add(row.client)
		self.clients = list(unique_rows)
		if duplicates:
			duplicate_client_names = set()
			for client in duplicates:
				# Get client title (instead of showing only ID like CLXSBN001)
				client_name = frappe.get_value("WMS Client", client, "client_name")
				duplicate_client_names.add(client_name)
			frappe.msgprint(
				_("Duplicate Member(s) found: {0}. Only updating unique clients.").format(
					frappe.bold(", ".join(duplicate_client_names))
				)
			)
