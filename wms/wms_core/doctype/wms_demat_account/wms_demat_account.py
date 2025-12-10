# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from wms.utils import calculate_age


class WMSDematAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_investment.doctype.wms_investment_holder.wms_investment_holder import WMSInvestmentHolder

		bank_account_number: DF.Data | None
		client: DF.Link
		client_id: DF.Data | None
		company_name: DF.Link
		demat_account_number: DF.Data | None
		dp_id: DF.Data
		dp_type: DF.Literal["CDSL", "NSDL"]
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		is_existing_demat: DF.Check
		nominees: DF.Table[WMSNominee]
		registered_bank: DF.Link | None
		status: DF.Literal["Opening Request", "Opened", "Request with DP", "Client Dependency"]
		through_us: DF.Check
		trading_id: DF.Data | None
	# end: auto-generated types
	pass

	def auto_name(self):
		if self.dp_id and self.client_id:
			self.demat_account_number = self.dp_id + self.client_id
			self.name = self.demat_account_number
		elif self.trading_id:
			self.name = self.trading_id

	def validate(self):
		self.validate_holders()
		self.validate_nominee()

	def validate_nominee(self):
		if self.nominees and len(self.nominees) > 0:
			holders = [holder.holder for holder in self.holders] if len(self.holders) > 0 else []
			share_percentage = 0
			for nominee in self.nominees:
				share_percentage += nominee.share_percent
				if nominee.nominee_name == self.client:
					frappe.throw("Client cannot be a nominee.")
				if nominee.nominee_name in holders:
					frappe.throw("Holder cannot be a nominee.")
				if nominee.dob:
					if calculate_age(nominee.dob) < 18:
						nominee.is_minor = 1
						if not nominee.guardian_name or not nominee.guardian_relation:
							frappe.throw("Guardian details are required for minor nominees.")
						if nominee.guardian_dob and calculate_age(nominee.guardian_dob) < 18:
							frappe.throw("Guardian must be at least 18 years old.")
						if nominee.guardian_name == self.client:
							frappe.throw("Client cannot be a guardian.")
						if nominee.nominee_name == nominee.guardian_name:
							frappe.throw("Nominee and Guardian cannot be the same person.")
						if nominee.guardian_name in holders:
							frappe.throw("Holder cannot be the guardian.")

			if share_percentage != 100:
				frappe.throw("Total share percentage of nominees must be 100%.")

	def validate_holders(self):
		if self.holders and len(self.holders) > 0:
			if self.holding_type == "Single":
				frappe.throw("Cannot add holders for Single Holding Type.")
			if len(self.holders) > 2:
				frappe.throw("You can only add a maximum of 2 holders.")
			for holder in self.holders:
				if holder.holder == self.client:
					frappe.throw("Client cannot be a holder.")
