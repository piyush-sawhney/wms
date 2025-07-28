# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WMSClient(Document):
	def before_save(self):
		self.update_classification_for_individuals()
		
	def validate(self):
		self.validate_client_name()
		self.validate_ubos()
		self.validate_bank_details()
		self.validate_phone_details()
		self.validate_emails()
	
	def validate_bank_details(self):
		if self.banks and len(self.banks) > 0:
			account_numbers = set()
			for bank in self.banks:
				if bank.account_number in account_numbers:
					frappe.throw(f"Duplicate Account Number: {bank.account_number}")
				account_numbers.add(bank.account_number)
	
	def validate_phone_details(self):
		if self.phone_numbers and len(self.phone_numbers) > 0:
			phone_numbers = set()
			for phone_number in self.phone_numbers:
				if phone_number.phone in phone_numbers:
					frappe.throw(f"Duplicate Phone Number: {phone_number.phone}")
				phone_numbers.add(phone_number.phone)
	
	def validate_emails(self):
		if self.email_ids and len(self.email_ids) > 0:
			email_ids = set()
			for email_id in self.email_ids:
				if email_id.email_id in email_ids:
					frappe.throw(f"Duplicate Email ID: {email_id.email_id}")
				email_ids.add(email_id.email_id)

	def validate_ubos(self):
		if self.type == "Individual" and self.classification =="Sole Proprietor":
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

def calculate_age(dob):
	dob_date = frappe.utils.getdate(dob)
	today = frappe.utils.nowdate()
	return frappe.utils.date_diff(today, dob_date) // 365
