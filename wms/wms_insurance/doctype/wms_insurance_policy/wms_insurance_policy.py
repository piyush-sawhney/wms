# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSInsurancePolicy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_insurance.doctype.wms_insurance_member.wms_insurance_member import WMSInsuranceMember

		chassis_number: DF.Data | None
		client: DF.Link | None
		date_of_registration: DF.Date | None
		desciption: DF.TextEditor | None
		end_date: DF.Date | None
		engine_number: DF.Data | None
		health_plan_name: DF.Data | None
		health_type: DF.Literal["Floater", "Individual", "Multi-Individual", "Top Up", "Super Top Up"]
		idv: DF.Float
		insurance_type: DF.Link | None
		is_existing_policy: DF.Check
		is_for_self: DF.Check
		life_plan_name: DF.Data | None
		members: DF.Table[WMSInsuranceMember]
		ncb: DF.Percent
		period: DF.Int
		plan_number: DF.Data | None
		policy_number: DF.Data | None
		ppt: DF.Int
		premium: DF.Float
		premium_mode: DF.Literal["Monthly", "Quarterly", "Half Yearly", "Yearly", "Single"]
		proposer: DF.Link | None
		provider: DF.Link | None
		quote_number: DF.Data | None
		renewed_policy: DF.Link | None
		start_date: DF.Date | None
		status: DF.Literal["Active", "Cancelled", "Expired", "Renewed"]
		sum_assured: DF.Float
		through_us: DF.Check
		tp_loading: DF.Percent
		vehicle_make: DF.Data | None
		vehicle_model: DF.Data | None
		vehicle_number: DF.Data | None
		vehicle_type: DF.Link | None
	# end: auto-generated types
	pass
