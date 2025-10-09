# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wms.utils import calculate_age

class WMSMFFolio(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_investment.doctype.wms_investment_holder.wms_investment_holder import WMSInvestmentHolder

		amc: DF.Link
		broker_code: DF.Data | None
		broker_name: DF.Link | None
		client: DF.Link
		folio_check_digits: DF.Int
		folio_created: DF.Check
		folio_number: DF.Data | None
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		is_existing_folio: DF.Check
		nominees: DF.Table[WMSNominee]
		through_broker: DF.Check
		through_us: DF.Check
	# end: auto-generated types
	pass

	def auto_name(self):
		if self.folio_number:
			self.name = self.folio_number


	def validate(self):
		self.validate_holders()
		self.validate_nominee()
		self.validate_folio_number()


	def validate_folio_number(self):
		if self.folio_number and self.folio_number != "New Folio":
			import re

			pattern = r"^\d+$"
			if bool(re.match(pattern, self.folio_number)) is False:
				frappe.throw(
					"Folio Number must be a number. Slash (/) and two digits should be entered in Folio Check Digits."
				)

			existing = frappe.db.exists(
            	self.doctype, {"folio_number": self.folio_number}
			)
			if existing:
				frappe.throw(f"Folio Number <b>{self.folio_number}</b> already exists in record.")

	def on_update(self):
		if self.folio_number and self.name != self.folio_number:
			self.folio_created = 1
			frappe.rename_doc(self.doctype, self.name, self.folio_number, merge=False)


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

