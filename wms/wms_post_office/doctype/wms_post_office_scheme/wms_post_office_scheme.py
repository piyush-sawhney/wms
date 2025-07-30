# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPostOfficeScheme(Document):
	 def autoname(self):
		 self.name = f"{self.code.strip().upper()}-{self.period}-{str(self.roi)}"
	 
