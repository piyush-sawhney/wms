# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe import _
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
		from wms.wms_investment.doctype.wms_po_extension.wms_po_extension import WMSPOExtension

		account_number: DF.Data | None
		amount: DF.Currency
		client: DF.Link
		client_classification: DF.Data | None
		client_name: DF.Data | None
		currency: DF.Link | None
		entry_date: DF.Date
		extend_investment: DF.Check
		extensions: DF.Table[WMSPOExtension]
		guardian: DF.Link | None
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		is_existing_investment: DF.Check
		is_partner_investment: DF.Check
		maturity_date: DF.Date | None
		nominees: DF.Table[WMSNominee]
		partner_name: DF.Data | None
		passbook_status: DF.Literal["Not Created", "With Us", "With Client", "With PO"]
		period: DF.Int
		rejected_reason: DF.Data | None
		renewed_investment: DF.DynamicLink | None
		renewed_investment_type: DF.Link | None
		roi: DF.Float
		scheme_code: DF.Data | None
		scheme_name: DF.Link
		start_date: DF.Date | None
		status: DF.Literal[
			"Entry Done",
			"Submitted",
			"Active",
			"Renewed",
			"Matured",
			"Pre-Matured",
			"Transmitted",
			"Rejected",
		]
		submit_branch: DF.Data | None
		through_us: DF.Check

	# end: auto-generated types
	def autoname(self):
		FY = get_financial_year_code(self.entry_date)
		self.name = make_autoname(f"PO-{FY}-.####")

	# def before_save(self):
	# 	self.update_status_for_rd_account_doctype()

	# def update_status_for_rd_account_doctype(self):
	# 	if self.status and self.account_number and self.scheme_code == "RD":
	# 		if frappe.db.exists('WMS RD Account', self.account_number):
	# 			frappe.db.set_value("WMS RD Account", self.account_number, 'status', self.status)

	def validate(self):
		self.validate_holders()
		self.validate_nominee()
		self.validate_dates()
		self.validate_minor_investment()
		self.validate_rejected_investment()

	def validate_rejected_investment(self):
		if self.status != "Rejected" and self.rejected_reason:
			self.rejected_reason = None

	def validate_minor_investment(self):
		if self.client_classification == "Minor":
			if self.guardian and self.guardian == self.client:
				frappe.throw(_("Guardian cannot be the client."))
			if self.holding_type != "Single":
				frappe.throw(_("Holding Type must be 'Single' for Minor clients."))

	def validate_nominee(self):
		if self.nominees and len(self.nominees) > 0:
			holders = [holder.holder for holder in self.holders] if len(self.holders) > 0 else []
			share_percentage = 0
			for nominee in self.nominees:
				share_percentage += nominee.share_percent
				if nominee.nominee_name == self.client:
					frappe.throw(_("Client cannot be a nominee."))
				if nominee.nominee_name in holders:
					frappe.throw(_("Holder cannot be a nominee."))
				if self.guardian and nominee.nominee_name == self.guardian:
					frappe.throw(_("Guardian cannot be a nominee."))
				if nominee.dob:
					if calculate_age(nominee.dob) < 18:
						nominee.is_minor = 1
						if not nominee.guardian_name or not nominee.guardian_relation:
							frappe.throw(_("Guardian details are required for minor nominees."))
						if nominee.guardian_dob and calculate_age(nominee.guardian_dob) < 18:
							frappe.throw(_("Guardian must be at least 18 years old."))
						if nominee.guardian_name == self.client:
							frappe.throw(_("Client cannot be a guardian."))
						if nominee.nominee_name == nominee.guardian_name:
							frappe.throw(_("Nominee and Guardian cannot be the same person."))
						if nominee.guardian_name in holders:
							frappe.throw(_("Holder cannot be the guardian."))

			if share_percentage != 100:
				frappe.throw(_("Total share percentage of nominees must be 100%."))

	def validate_holders(self):
		if self.holders and len(self.holders) > 0:
			if self.holding_type == "Single":
				frappe.throw(_("Cannot add holders for Single Holding Type."))
			if len(self.holders) > 2:
				frappe.throw(_("You can only add a maximum of 2 holders."))
			for holder in self.holders:
				if holder.holder == self.client:
					frappe.throw(_("Client cannot be a holder."))

	def validate_dates(self):
		now_date = nowdate()
		if self.entry_date and str(self.entry_date) > now_date:
			frappe.throw(_("Entry Date cannot be in the future."))
		if self.start_date:
			if str(self.start_date) > now_date:
				frappe.throw(_("Start Date cannot be in the future."))
			if self.extend_investment and len(self.extensions) > 0:
				latest = sorted(self.extensions, key=lambda x: x.extension_date, reverse=True)[0]
				if len(self.extensions) > 1:
					previous = sorted(self.extensions, key=lambda x: x.extension_date, reverse=True)[1]
					if str(latest.extension_date) < str(previous.extension_date):
						frappe.throw(_("Latest Extension Date cannot be before previous Extension Date"))
				elif str(latest.extension_date) < str(add_months(self.start_date, self.period)):
					frappe.throw(_("Extension Date cannot be before Maturity Date"))
				self.maturity_date = add_months(latest.extension_date, latest.extension_period)
			else:
				self.maturity_date = add_months(self.start_date, self.period)
		else:
			self.maturity_date = None
