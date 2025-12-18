# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WMSMFTransaction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		all_units: DF.Check
		amount: DF.Currency
		broker_code: DF.Data | None
		broker_name: DF.Link | None
		client_name: DF.Data | None
		currency: DF.Link | None
		entry_date: DF.Date
		folio_number: DF.Link
		name: DF.Int | None
		rejected_reason: DF.Data | None
		request_type: DF.Literal["New Purchase", "Additional Purchase", "SIP", "Redemption", "Switch", "STP", "SWP"]
		scheme: DF.Link
		scheme_name: DF.Data | None
		scheme_out: DF.Link | None
		start_date: DF.Date | None
		status: DF.Literal["Entry Done", "Submitted", "Investment Created", "Dependency on Client", "Pending With Us", "Rejected"]
		through_broker: DF.Check
		through_us: DF.Check
		units: DF.Float
	# end: auto-generated types
	pass

	def validate(self):
		self.validate_units_or_amount()
		self.validate_scheme()

	def validate_scheme(self):
		if self.scheme_out and self.scheme == self.scheme_out:
			frappe.throw("Scheme and Scheme Out cannot be the same.")

	def validate_units_or_amount(self):
		if not self.all_units and not self.amount and not self.units:
			frappe.throw("Please enter either Units or Amount.")
		if self.all_units and (self.amount or self.units):
			frappe.throw("Please enter only one of Units, Amount or All Units.")
		if self.amount and self.units:
			frappe.throw("Please enter only one of Amount or Units.")
