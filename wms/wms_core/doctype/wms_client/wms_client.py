# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import random
import string
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from wms.utils import calculate_age


class WMSClient(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.contacts.doctype.contact_email.contact_email import ContactEmail
		from frappe.contacts.doctype.contact_phone.contact_phone import ContactPhone
		from frappe.types import DF
		from wms.wms_core.doctype.wms_client_codes.wms_client_codes import WMSClientCodes
		from wms.wms_core.doctype.wms_ubo.wms_ubo import WMSUBO

		classification: DF.Link
		client_group: DF.Link | None
		client_name: DF.Data
		codes: DF.Table[WMSClientCodes]
		dob: DF.Date | None
		email_addresses: DF.Table[ContactEmail]
		nps_pran: DF.Data | None
		numbers: DF.Table[ContactPhone]
		pan: DF.Link | None
		pob: DF.Data | None
		post_office_cif: DF.Data | None
		primary_email: DF.Data | None
		primary_mobile: DF.Data | None
		proprietor: DF.Link | None
		type: DF.Data | None
		ubos: DF.Table[WMSUBO]
		uuid: DF.Data | None
	# end: auto-generated types
	def onload(self):
		load_address_and_contact(self)

	def on_trash(self):
		delete_contact_and_address("WMS Client", self.name)


	def autoname(self):
		random_letters = ''.join(random.choices(string.ascii_uppercase, k=4))
		self.name = make_autoname(f"CL{random_letters}.###")
	
	def after_insert(self):
		create_contact(self)
				
	def before_save(self):
		self.update_classification_for_individuals()

	def validate(self):
		self.validate_client_name()
		self.validate_ubos()
		self.validate_pan_type_combination()
		self.validate_dob()
		self.validate_sole_proprietor()
		self.validate_primary_email()
		self.validate_primary_mobile()

	def validate_primary_email(self):
		pass
	
	def validate_primary_mobile(self):
		pass
	
	
	def validate_sole_proprietor(self):
		if self.type == "Individual" and self.classification == "Sole Proprietor":
			if not self.proprietor:
				frappe.throw("Proprietor Details are mandatory for Sole Proprietorship.")
	
	
	def validate_pan_type_combination(self):
		if not self.type or not self.pan:
			return
		type_to_pan_code = {
			"Individual": "P",
			"Body of Individuals (BOI)": "B",
			"Association of Persons (AOP)": "A",
			"Hindu Undivided Family (HUF)": "H",
			"Company": "C",
			"Limited Liability Partnership (LLP)": "E",
			"Partnership Firm": "F",
			"Trust": "T",
			"Government Agency": "G",
			"Local Authority": "L",
			"Artificial Judicial Person": "J",
		}
		expected_code = type_to_pan_code.get(self.type)
		actual_code = self.pan[3]
		if actual_code != expected_code:
			frappe.throw(
				f"PAN does not match the selected type '{self.type}'. "
				f"The 4th character should be '{expected_code}', but found '{actual_code}'."
			)

	def validate_dob(self):
		if self.dob:
			dob_date = frappe.utils.getdate(self.dob)
			today = frappe.utils.getdate(frappe.utils.nowdate())
			if dob_date > today:
				frappe.throw("Date of Birth/Incorporation cannot be in the future.")

	def validate_ubos(self):
		if self.type != "Individual":
			if self.type == "Hindu Undivided Family (HUF)" and len(self.ubos) != 1:
				frappe.throw("Enter single karta details for the HUF")
			elif len(self.ubos) < 1:
				frappe.throw("At least one beneficiary required for Non-Individual Clients")

	def validate_client_name(self):
		if not self.client_name:
			frappe.throw("Client Name is mandatory")
		if len(self.client_name) < 3:
			frappe.throw("Client Name must be at least 3 characters long")

	def update_classification_for_individuals(self):
		if self.dob and self.type == "Individual" and self.classification != "Sole Proprietor":
			age = calculate_age(self.dob)
			if age < 18:
				if self.classification != "Minor":
					self.classification = "Minor"
					frappe.msgprint("Classification updated to Minor based on age.")
			elif age >= 18 and self.classification == "Minor":
				frappe.throw("Minor cannot be greater than 18 years old. ")

def create_contact(args):
	values = {
		"doctype": "Contact",
		"links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
	}


	if args.type == "Individual":
		first, middle, last = parse_full_name(args.client_name)
		values.update(
			{
				"first_name": first,
				"middle_name": middle,
				"last_name": last,
			}
		)
	else:
		values.update(
			{
				"company_name": args.client_name,
			}
		)
	contact = frappe.get_doc(values)
	contact.insert(ignore_permissions=True)
	


def parse_full_name(full_name: str) -> tuple[str, str | None, str | None]:
	"""Parse full name into first name, middle name and last name"""
	names = full_name.split()
	first_name = names[0]
	middle_name = " ".join(names[1:-1]) if len(names) > 2 else None
	last_name = names[-1] if len(names) > 1 else None

	return first_name, middle_name, last_name
