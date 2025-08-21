# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt
import random
import string
import frappe
from frappe import _

from frappe.model.document import Document
from frappe.model.naming import make_autoname

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
		random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
		self.name = make_autoname(f"FAM{random_letters}.###")

	def validate(self):
		self.validate_members()

	def _validate_member_in_another_family(self):
		for family_member in self.family_members:
			if not family_member.member_contact:
				continue

			# Get member title (instead of showing only ID like CLXSBN001)
			member_title = frappe.get_value("WMS Client", family_member.member_contact, "client_name")

			# Fetch all families where this member already exists (excluding current one)
			existing_members = frappe.get_all(
				"WMS Family Member",
				filters={
					"member_contact": family_member.member_contact,
					"parent": ["!=", self.name],
				},
				fields=["parent"],
				distinct=True,
			)

			if existing_members:
				# Collect family names in one go
				family_ids = [f.parent for f in existing_members]
				families = frappe.get_all(
					"WMS Family",
					filters={"name": ["in", family_ids]},
					fields=["name"],
				)
				family_titles = [
					frappe.get_doc("WMS Family", f.name).get_title() for f in families
				]

				frappe.msgprint(
					_("Member {0} is also part of {1}.").format(
						frappe.bold(member_title),
						frappe.bold(", ".join(family_titles))
					)
				)
				

	def validate_members(self):
		if not self.family_members:
			frappe.throw("Cannot create a family without any family members.")

		family_members = set()
		for index, family_member in enumerate(self.family_members):
			if not family_member.member_contact:
				frappe.throw(
					f"All family members must be linked to a contact. Missing link for: {index + 1} row."
				)

			if family_member.member_contact in family_members:
				frappe.throw(
					f"Same family member cannot be added multiple times: {family_member.member_name}"
				)

			family_members.add(family_member.member_contact)

		self._validate_member_in_another_family()
