# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import random
import string

import frappe
from frappe import _
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from frappe.model.document import Document
from frappe.model.naming import make_autoname

from wms.utils import calculate_age


class WMSClient(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.contacts.doctype.contact_email.contact_email import ContactEmail
		from frappe.types import DF

		from wms.wms_core.doctype.wms_client_codes.wms_client_codes import WMSClientCodes
		from wms.wms_core.doctype.wms_phone_number.wms_phone_number import WMSPhoneNumber
		from wms.wms_core.doctype.wms_ubo.wms_ubo import WMSUBO

		classification: DF.Link
		client_image: DF.AttachImage | None
		client_name: DF.Data
		codes: DF.Table[WMSClientCodes]
		dob: DF.Date | None
		email_addresses: DF.Table[ContactEmail]
		is_whatsapp_no: DF.Check
		label: DF.Data | None
		pan: DF.Link | None
		phone_numbers: DF.Table[WMSPhoneNumber]
		pob: DF.Data | None
		primary_email: DF.Data | None
		primary_mobile: DF.Phone | None
		proprietor: DF.Link | None
		status: DF.Literal["Active", "Inactive", "Deceased"]
		type: DF.Data | None
		ubos: DF.Table[WMSUBO]
		uuid: DF.Data | None
		whatsapp_number: DF.Phone | None

	# end: auto-generated types
	def onload(self):
		load_address_and_contact(self)

	def on_trash(self):
		delete_contact_and_address("WMS Client", self.name)

	def autoname(self):
		random_letters = "".join(random.choices(string.ascii_uppercase, k=4))
		self.name = make_autoname(f"CL{random_letters}.###")

	def before_save(self):
		self.update_classification_for_individuals()

	def validate_multiple_pans(self):
		if self.pan:
			list_of_client_with_pan = frappe.db.get_list(
				"WMS Client", filters={"name": ["!=", self.name], "pan": self.pan}, pluck="client_name"
			)
			if list_of_client_with_pan:
				frappe.msgprint(
					msg=list_of_client_with_pan,
					title="Clients with same PAN that exists in the system.",
					as_list=True,
				)

	def validate(self):
		self.validate_client_name()
		self.validate_ubos()
		self.validate_pan_type_combination()
		self.validate_dob()
		self.validate_sole_proprietor()
		self.validate_primary_email()
		self.validate_phone_numbers()

	def validate_phone_numbers(self):
		self._normalize_numbers()
		self.validate_unique_phone_numbers()

		if self.is_new():
			self._build_table_from_fields()
		else:
			self._sync_fields_and_table()

	# ---------------------------------------
	# 1. NORMALIZATION
	# ---------------------------------------

	def _normalize_numbers(self):
		if self.primary_mobile == "+91-":
			self.primary_mobile = None
		if self.whatsapp_number == "+91-":
			self.whatsapp_number = None

	# ---------------------------------------
	# 2. UNIQUE VALIDATION
	# ---------------------------------------

	def validate_unique_phone_numbers(self):
		seen = set()
		for row in self.phone_numbers:
			phone = (row.phone or "").strip()
			if phone and phone in seen:
				frappe.throw(_(f"Duplicate Phone Number: {frappe.bold(phone)}"))
			seen.add(phone)

	# ---------------------------------------
	# 3A. NEW DOCUMENT LOGIC
	# ---------------------------------------

	def _build_table_from_fields(self):
		pm = (self.primary_mobile or "").strip()
		wa = (self.whatsapp_number or "").strip()
		is_wa_primary = bool(self.is_whatsapp_no)

		if pm:
			# CASE A: primary exists
			if is_wa_primary:
				wa = pm
				self.whatsapp_number = pm
				self._add_row(pm, phone=1, wa=1)
			else:
				if wa:
					if pm == wa:
						self.is_whatsapp_no = 1
						self._add_row(pm, phone=1, wa=1)
					else:
						self._add_row(pm, phone=1)
						self._add_row(wa, wa=1)
				else:
					self._add_row(pm, phone=1)

		elif wa:
			# CASE B: only whatsapp provided
			self.primary_mobile = wa
			self.is_whatsapp_no = 1
			self._add_row(wa, phone=1, wa=1)

	# ---------------------------------------
	# 3B. EXISTING DOCUMENT LOGIC
	# ---------------------------------------

	def _sync_fields_and_table(self):
		table = list(self.phone_numbers)

		if not table:
			self._sync_no_table_case()
			return

		self._sync_primary(table)
		self._sync_whatsapp(table)

	# ---------------------------------------
	# PRIMARY LOGIC
	# ---------------------------------------

	def _sync_primary(self, table):
		primary_rows = [r for r in table if r.is_primary_phone]

		if len(primary_rows) != 1:
			frappe.throw(
				_("There must be exactly {}  Primary Number in the table.".format(frappe.bold(_("One"))))
			)

		table_primary = (primary_rows[0].phone or "").strip()

		if (self.primary_mobile or "").strip() != table_primary:
			self.primary_mobile = table_primary

	# ---------------------------------------
	# WHATSAPP LOGIC
	# ---------------------------------------

	def _sync_whatsapp(self, table):
		whatsapp_rows = [r for r in table if r.is_primary_whatsapp]
		db_has_whatsapp = bool(frappe.get_value(self.doctype, self.name, "whatsapp_number"))

		# CASE 1: database HAS whatsapp
		if db_has_whatsapp:
			self._sync_whatsapp_when_db_has_value(whatsapp_rows)
			return

		# CASE 2: database does NOT have whatsapp
		self._sync_whatsapp_when_db_empty(whatsapp_rows, table)

	def _sync_whatsapp_when_db_has_value(self, whatsapp_rows):
		if not whatsapp_rows:
			self.whatsapp_number = None
			self.is_whatsapp_no = 0
			return

		if len(whatsapp_rows) != 1:
			frappe.throw(
				_("There must be exactly {}  Primary Whatsapp in the table.".format(frappe.bold(_("One"))))
			)

		table_wa = (whatsapp_rows[0].phone or "").strip()

		if table_wa != (self.whatsapp_number or "").strip():
			self.whatsapp_number = table_wa

		self.is_whatsapp_no = int(self.whatsapp_number == self.primary_mobile)

	def _sync_whatsapp_when_db_empty(self, whatsapp_rows, table):
		# CASE A: no whatsapp in table
		if not whatsapp_rows:
			if self.is_whatsapp_no:
				self.whatsapp_number = self.primary_mobile
				self._mark_whatsapp(self.whatsapp_number, table)
			elif self.whatsapp_number:
				self._mark_whatsapp(self.whatsapp_number, table)
			return

		# CASE B: table has whatsapp
		if len(whatsapp_rows) != 1:
			frappe.throw(
				_("There must be exactly {}  Primary Whatsapp in the table.".format(frappe.bold(_("One"))))
			)

		table_wa = (whatsapp_rows[0].phone or "").strip()
		self.whatsapp_number = table_wa
		self._mark_whatsapp(table_wa, table)
		self.is_whatsapp_no = int(self.whatsapp_number == self.primary_mobile)

	# ---------------------------------------
	# HELPERS
	# ---------------------------------------

	def _add_row(self, number, phone=0, wa=0):
		self.append(
			"phone_numbers",
			{
				"phone": number,
				"is_primary_phone": phone,
				"is_primary_whatsapp": wa,
			},
		)

	def _mark_whatsapp(self, number, table):
		found = False
		for row in table:
			row_no = (row.phone or "").strip()
			row.is_primary_whatsapp = int(row_no == number)
			if row_no == number:
				found = True
		if not found:
			self._add_row(number, wa=1)

	def _sync_no_table_case(self):
		db_primary_exists = bool(frappe.get_value(self.doctype, self.name, "primary_mobile"))

		if db_primary_exists:
			# DB has primary → clear fields
			self.primary_mobile = None
			self.whatsapp_number = None
		else:
			self._build_table_from_fields()

	def validate_primary_email(self):
		"""Keep primary_email field in sync with child table."""
		is_primary_email_set = (
			True if bool(frappe.get_value(self.doctype, self.name, "primary_email")) else False
		)
		if not self.email_addresses:
			if is_primary_email_set:
				# Case when deleting all the child table rows
				self.primary_email = None
				self.flags.is_primary_email_set = False
				return
			if not is_primary_email_set and self.primary_email:
				self.append(
					"email_addresses",
					{
						"email_id": self.primary_email,
						"is_primary": 1,
					},
				)
				self.flags.is_primary_email_set = True
				return
		else:
			primary_rows = [e for e in self.email_addresses if e.is_primary]

			if len(primary_rows) != 1:
				frappe.throw(
					_("There must be exactly {} primary email in the table.".format(frappe.bold(_("One"))))
				)

			# Sync field from table primary
			table_primary = (primary_rows[0].email_id or "").strip()
			if table_primary != (self.primary_email or "").strip():
				self.primary_email = table_primary


	def validate_sole_proprietor(self):
		if self.type == "Individual" and self.classification == "Sole Proprietor":
			if not self.proprietor:
				frappe.throw("Proprietor Details are mandatory for Sole Proprietorship.")

	def validate_pan_type_combination(self):
		if not self.type or not self.pan:
			return
		self.validate_multiple_pans()
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
