# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WMSFamily(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_family_member.wms_family_member import WMSFamilyMember

		family_head: DF.Link
		family_members: DF.Table[WMSFamilyMember]
		family_name: DF.Data
	# end: auto-generated types
	def autoname(self):
		while True:
			name = frappe.generate_hash(length=10).upper()

			if not frappe.db.exists(self.doctype, name):
				self.name = name
				break

	def validate(self):
		self.validate_members()



	def validate_member_in_another_family(self):
		for family_member in self.family_members:
			if family_member.member_contact:
				# First check in child table where this contact exists
				existing_members = frappe.get_all(
					"WMS Family Member",  # The child table Doctype name
					filters={
						"member_contact": family_member.member_contact,
						"parent": ["!=", self.name]
					},
					fields=["parent"]
				)

				if existing_members:
					family_names = ", ".join([f.parent for f in existing_members])
					frappe.msgprint (
						f"Member <b>{family_member.member_contact}</b> is also part of <b>{family_names}</b> family(ies)."
					)

	def validate_members(self):
		if not self.family_members:
			frappe.throw("Cannot create a family without any family members.")
	
		family_members = set()
		for index,family_member in enumerate(self.family_members):
			if not family_member.member_contact:
				frappe.throw(f"All family members must be linked to a contact. Missing link for: {index + 1} row.")

			if family_member.member_contact in family_members:
				frappe.throw(f"Same family member cannot be added multiple times: {family_member.member_name}")
		
			family_members.add(family_member.member_contact)
	
		self.validate_member_in_another_family()