# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSFamily(Document):
	def before_save(self):
		self.format_fields()

	def format_fields(self):
		self.family_name = self.family_name.strip().title()
	# TODO:Implement unique family members in a family. 
	# TODO:If a member is already present in the family, it can be added in another family but with a message that this member is already present in another family.