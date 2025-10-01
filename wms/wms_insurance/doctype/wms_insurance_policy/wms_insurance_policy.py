# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import add_days, add_months, add_years, nowdate

from wms.utils import calculate_age, get_financial_year_code


class WMSInsurancePolicy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_insurance.doctype.wms_insurance_member.wms_insurance_member import WMSInsuranceMember

		chassis_number: DF.Data | None
		client: DF.Link | None
		currency: DF.Link | None
		date_of_registration: DF.Date | None
		desciption: DF.TextEditor | None
		discount: DF.Percent
		maturity_date: DF.Date | None
		engine_number: DF.Data | None
		entity_item: DF.DynamicLink | None
		entity_type: DF.Link | None
		entry_date: DF.Date
		health_plan_name: DF.Data | None
		health_type: DF.Literal["Floater", "Individual", "Multi-Individual", "Top Up", "Super Top Up"]
		idv: DF.Float
		insurance_type: DF.Link
		is_existing_policy: DF.Check
		is_for_self: DF.Check
		life_plan_name: DF.Data | None
		members: DF.Table[WMSInsuranceMember]
		ncb: DF.Percent
		nominees: DF.Table[WMSNominee]
		period: DF.Int
		period_type: DF.Literal["Days", "Months", "Years"]
		plan_number: DF.Data | None
		policy_number: DF.Data | None
		ppt: DF.Int
		premium: DF.Currency
		premium_mode: DF.Literal["Monthly", "Quarterly", "Half Yearly", "Yearly", "Single"]
		proposer: DF.Link
		provider: DF.Link
		quote_number: DF.Data | None
		renewed_policy: DF.Link | None
		start_date: DF.Date | None
		status: DF.Literal["Proposal", "Active", "Cancelled", "Expired", "Renewed", "Rejected"]
		sum_assured: DF.Currency
		sum_assured_currency: DF.Link | None
		through_us: DF.Check
		tp_loading: DF.Percent
		vehicle_make: DF.Data | None
		vehicle_model: DF.Data | None
		vehicle_number: DF.Data | None
		vehicle_type: DF.Literal["Private Car", "Two Wheeler", "Commercial"]
	# end: auto-generated types
	pass

	def autoname(self):
		FY = get_financial_year_code(self.entry_date)
		self.name = make_autoname(f"INS-{FY}-.####")

	def validate(self):
		self.validate_client()
		self.validate_nominee()
		self.validate_dates()
		self.validate_life_insurance()
		self.validate_health_insurance()
		self.validate_vehicle_insurance()
		self.validate_other_insurance()

	def validate_other_insurance(self):
		if self.insurance_type not in ["Vehicle Insurance", "Health Insurance", "Life Insurance"]:
			if not self.desciption:
				frappe.throw("Description is required for other types of insurance policies.")

	def validate_vehicle_insurance(self):
		if self.insurance_type == "Vehicle Insurance" and self.is_existing_policy != 1:
			if not self.vehicle_number:
				frappe.throw("Vehicle Number is required for Vehicle Insurance policies.")
			if not self.vehicle_type:
				frappe.throw("Vehicle Type is required for Vehicle Insurance policies.")

	def validate_health_insurance(self):
		if self.insurance_type == "Health Insurance" and self.is_existing_policy != 1:
			if not self.health_plan_name:
				frappe.throw("Plan Name is required for Health Insurance policies.")
			if self.health_type not in [
				"Floater",
				"Individual",
				"Multi-Individual",
				"Top Up",
				"Super Top Up",
			]:
				frappe.throw(
					"Invalid Health Type. Choose from Floater, Individual, Multi-Individual, Top Up, or Super Top Up."
				)
			if (self.health_type == "Floater" or self.health_type == "Multi-Individual") and not self.members:
				frappe.throw(
					"Members are required for Floater or Multi Individual Health Insurance policies."
				)

	def validate_life_insurance(self):
		if self.insurance_type == "Life Insurance" and self.is_existing_policy != 1:
			if not self.life_plan_name:
				frappe.throw("Life Plan Name is required for Life Insurance policies.")
			if not self.ppt:
				frappe.throw("Premium Payment Term (PPT) is required for Life Insurance policies.")
			if not self.premium_mode:
				frappe.throw("Premium Mode is required for Life Insurance policies.")

	def validate_nominee(self):
		if self.nominees and len(self.nominees) > 0:
			share_percentage = 0
			for nominee in self.nominees:
				share_percentage += nominee.share_percent
				if nominee.nominee_name == self.client:
					frappe.throw("Client cannot be a nominee.")
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

			if share_percentage != 100:
				frappe.throw("Total share percentage of nominees must be 100%.")

	def validate_client(self):
		if self.is_for_self:
			self.client = self.proposer
		else:
			if not self.client:
				frappe.throw("Person Assured is required when the policy is not for self.")

	def validate_dates(self):
		now_date = nowdate()
		if self.entry_date and self.entry_date > now_date:
			frappe.throw("Entry Date cannot be in the future.")

		if self.start_date:
			if self.period_type == "Days":
				self.maturity_date = add_days(self.start_date, self.period)
			elif self.period_type == "Months":
				self.maturity_date = add_months(self.start_date, self.period)
			elif self.period_type == "Years":
				self.maturity_date = add_years(self.start_date, self.period)
			self.maturity_date = add_days(self.maturity_date, -1)
		else:
			self.maturity_date = None
