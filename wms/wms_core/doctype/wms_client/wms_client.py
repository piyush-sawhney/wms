# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

from wms.utils import calculate_age


class WMSClient(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from wms.wms_core.doctype.wms_client_codes.wms_client_codes import WMSClientCodes
		from wms.wms_core.doctype.wms_ubo.wms_ubo import WMSUBO

		classification: DF.Link
		client_name: DF.Data
		codes: DF.Table[WMSClientCodes]
		dob: DF.Date | None
		gender: DF.Literal["Male", "Female", "Others"]
		nps_pran: DF.Data | None
		pan: DF.Link | None
		pob: DF.Data | None
		post_office_cif: DF.Data | None
		type: DF.Data | None
		ubos: DF.Table[WMSUBO]
		uuid: DF.Data | None
	# end: auto-generated types

	def autoname(self):
		self.name = self.create_name()

	def before_save(self):
		self.update_classification_for_individuals()

	def validate(self):
		self.validate_client_name()
		self.validate_ubos()
		self.validate_pan_type_combination()
		self.validate_dob()
		self.rename_client()

	def create_name(self):
		name_part = frappe.scrub(self.client_name).upper()  # Remove unsafe chars
		if self.classification == "Sole Proprietor" and self.pan:
			created_name = make_autoname(f"{name_part}-{self.pan.upper()}-.###")
		elif self.pan:
			created_name = f"{name_part}-{self.pan.upper()}"
		else:
			while True:
				random_hash = frappe.generate_hash(length=5).upper()
				name = f"{name_part}-{random_hash}"
				if not frappe.db.exists(self.doctype, name):
					created_name = name
					break
		return created_name

	def rename_client(self):
		if self.is_new() or frappe.flags.in_insert:
			return  # Do not rename during first insert\new_name = self.create_name()
		new_name = self.create_name()
		if self.name == new_name:
			return
		if self.pan and self.pan.upper() not in self.name:
			frappe.rename_doc(self.doctype, self.name, new_name, force=True)
			self.name = new_name
			return
		if self.name.split("-")[0] != new_name.split("-")[0]:
			frappe.rename_doc(self.doctype, self.name, new_name, force=True)
			self.name = new_name

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
		if self.type == "Individual" and self.classification == "Sole Proprietor":
			if len(self.ubos) != 1:
				frappe.throw("Enter Single Proprietor details in Beneficiaries Table")
		elif self.type != "Individual":
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
