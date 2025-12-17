# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSMFInvestorFolioSchemeMaster(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		aadhar_status: DF.Data | None
		amc_code: DF.Date | None
		balance_date: DF.Date | None
		bank_account_number: DF.Data | None
		bank_account_type: DF.Data | None
		bank_address_1: DF.Data | None
		bank_address_2: DF.Data | None
		bank_address_3: DF.Data | None
		bank_branch: DF.Data | None
		bank_city: DF.Data | None
		bank_ifsc: DF.Data | None
		bank_name: DF.Data | None
		bank_pincode: DF.Data | None
		broker_code: DF.Data | None
		dp_id: DF.Data | None
		email: DF.Data | None
		first_holder: DF.Data | None
		first_holder_address_1: DF.Data | None
		first_holder_address_2: DF.Data | None
		first_holder_address_3: DF.Data | None
		first_holder_city: DF.Data | None
		first_holder_ckyc: DF.Data | None
		first_holder_country: DF.Data | None
		first_holder_dob: DF.Date | None
		first_holder_fatca: DF.Check
		first_holder_father_name: DF.Data | None
		first_holder_mother_name: DF.Data | None
		first_holder_pan: DF.Data | None
		first_holder_pincode: DF.Data | None
		first_holder_state: DF.Data | None
		first_nominee_address_1: DF.Data | None
		first_nominee_address_2: DF.Data | None
		first_nominee_address_3: DF.Data | None
		first_nominee_city: DF.Data | None
		first_nominee_dob: DF.Date | None
		first_nominee_email: DF.Data | None
		first_nominee_id_number: DF.Data | None
		first_nominee_id_type: DF.Data | None
		first_nominee_mobile: DF.Data | None
		first_nominee_name: DF.Data | None
		first_nominee_percentage: DF.Float
		first_nominee_pincode: DF.Data | None
		first_nominee_relation: DF.Data | None
		first_nominee_state: DF.Data | None
		folio_created_date: DF.Date | None
		folio_creation_date: DF.Date | None
		folio_number: DF.Data | None
		gst_state_code: DF.Data | None
		guardian_ckyc: DF.Data | None
		guardian_dob: DF.Date | None
		guardian_fatca: DF.Check
		guardian_name: DF.Data | None
		guardian_pan: DF.Data | None
		holding_nature: DF.Data | None
		is_demat: DF.Check
		mobile: DF.Data | None
		occupation: DF.Data | None
		old_folio_number: DF.Data | None
		phone_office: DF.Data | None
		phone_residence: DF.Data | None
		reinvestment_flag: DF.Data | None
		remarks: DF.SmallText | None
		rta: DF.Literal["CAMS", "KFINTECH"]
		ruppee_balance: DF.Currency
		scheme_code: DF.Data | None
		scheme_folio_number: DF.Data | None
		scheme_name: DF.Data | None
		second__holder_pan: DF.Data | None
		second_holder_ckyc: DF.Data | None
		second_holder_dob: DF.Date | None
		second_holder_fatca: DF.Check
		second_holder_name: DF.Data | None
		second_nominee_address_1: DF.Data | None
		second_nominee_address_2: DF.Data | None
		second_nominee_address_3: DF.Data | None
		second_nominee_city: DF.Data | None
		second_nominee_dob: DF.Date | None
		second_nominee_email: DF.Data | None
		second_nominee_id_number: DF.Data | None
		second_nominee_id_type: DF.Data | None
		second_nominee_mobile: DF.Data | None
		second_nominee_name: DF.Data | None
		second_nominee_percentage: DF.Float
		second_nominee_pincode: DF.Data | None
		second_nominee_relation: DF.Data | None
		second_nominee_state: DF.Data | None
		sub_broker_dealer_code: DF.Data | None
		tax_status: DF.Data | None
		third_holder_ckyc: DF.Data | None
		third_holder_dob: DF.Date | None
		third_holder_fatca: DF.Check
		third_holder_name: DF.Data | None
		third_holder_pan: DF.Data | None
		third_nominee_address_1: DF.Data | None
		third_nominee_address_2: DF.Data | None
		third_nominee_address_3: DF.Data | None
		third_nominee_city: DF.Data | None
		third_nominee_dob: DF.Date | None
		third_nominee_email: DF.Data | None
		third_nominee_id_number: DF.Data | None
		third_nominee_id_type: DF.Data | None
		third_nominee_mobile: DF.Data | None
		third_nominee_name: DF.Data | None
		third_nominee_percentage: DF.Float
		third_nominee_pincode: DF.Data | None
		third_nominee_relation: DF.Data | None
		third_nominee_state: DF.Data | None
		tpa_linked: DF.Data | None
		tpin: DF.Data | None
		unit_balance: DF.Data | None
	# end: auto-generated types
	pass
