# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wms.utils import calculate_age, get_financial_year_code
from frappe.model.naming import make_autoname

class WMSMFInvestment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_investment.doctype.wms_investment_holder.wms_investment_holder import WMSInvestmentHolder

		all_units: DF.Check
		amount: DF.Currency
		broker_name: DF.Link | None
		client: DF.Link
		company: DF.Link
		currency: DF.Link | None
		entry_date: DF.Date
		folio_number: DF.Data | None
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		is_existing_folio: DF.Check
		nominees: DF.Table[WMSNominee]
		request_type: DF.Literal["New Purchase", "Additional Purchase", "SIP", "Redemption", "Switch", "STP", "SWP"]
		scheme: DF.Link
		scheme_out: DF.Link | None
		status: DF.Literal["Entry Done", "Submitted", "Investment Created", "Dependency on Client", "Pending With Us"]
		through_broker: DF.Check
		through_us: DF.Check
		units: DF.Float
	# end: auto-generated types
	pass

	def autoname(self):
		FY = get_financial_year_code(self.entry_date)
		self.name = make_autoname(f'MF-{FY}-.####')

	def validate(self):
		self.validate_holders()
		self.validate_nominee()
		self.validate_units_or_amount()
		self.validate_folio_number()
		self.validate_existing_folio()
	
	def validate_existing_folio(self):
		if self.request_type != "New Purchase":
			self.is_existing_folio = 1
		
	def validate_folio_number(self):
		if self.is_existing_folio and not self.folio_number:
			frappe.throw("Folio Number is required for existing folios.")
		if not self.is_existing_folio and self.folio_number:
			frappe.throw("Folio Number should not be provided for new folios.")
		import re
		pattern = r'^\d+(\/\d{2})?$'
		if bool(re.match(pattern, self.folio_number)) is False:
			frappe.throw("Folio Number must be a number or a number followed by a slash and two digits (e.g., 12563/45).")

	def validate_scheme(self):
		if not self.scheme:
			frappe.throw("Scheme is required.")
		if self.scheme_out and self.scheme == self.scheme_out:
			frappe.throw("Scheme and Scheme Out cannot be the same.")
	def validate_units_or_amount(self):
		if not self.all_units and not self.amount and not self.units:
			frappe.throw("Please enter either Units or Amount.")
		if self.all_units and (self.amount or self.units):
			frappe.throw("Please enter only one of Units, Amount or All Units.")
		if self.amount and self.units:
			frappe.throw("Please enter only one of Amount or Units.")

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
