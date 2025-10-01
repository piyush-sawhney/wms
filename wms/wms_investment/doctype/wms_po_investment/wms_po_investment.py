# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import add_months, nowdate

from wms.utils import calculate_age, get_financial_year_code


class WMSPOInvestment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_investment.doctype.wms_investment_holder.wms_investment_holder import WMSInvestmentHolder

		account_number: DF.Data | None
		amount: DF.Currency
		client: DF.Link
		currency: DF.Link | None
		entry_date: DF.Date
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		is_active: DF.Check
		is_existing_investment: DF.Check
		maturity_date: DF.Date | None
		nominees: DF.Table[WMSNominee]
		period: DF.Int
		renewed_investment: DF.DynamicLink | None
		renewed_investment_type: DF.Link | None
		roi: DF.Float
		scheme_code: DF.Data | None
		scheme_name: DF.Link
		start_date: DF.Date | None
		status: DF.Literal["Entry Done", "Submitted to PO", "Passbook Received", "Passbook Sent to Customer", "Renewed", "Matured", "Pre-Matured", "Transmitted"]
		through_us: DF.Check
	# end: auto-generated types
	def autoname(self):
		FY = get_financial_year_code(self.entry_date)
		self.name = make_autoname(f"PO-{FY}-.####")

	def validate(self):
		self.validate_holders()
		self.validate_nominee()
		self.validate_dates()
		self.validate_is_active()

	def validate_is_active(self):
		if self.status in ["Renewed", "Matured", "Pre-Matured", "Transmitted"]:
			self.is_active = 0

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

	def validate_dates(self):
		now_date = nowdate()
		if self.entry_date and self.entry_date > now_date:
			frappe.throw("Entry Date cannot be in the future.")

		if self.start_date:
			if self.start_date > now_date:
				frappe.throw("Start Date cannot be in the future.")
			self.maturity_date = add_months(self.start_date, self.period)
		else:
			self.maturity_date = None
