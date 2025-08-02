# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPOScheme(Document):
        def autoname(self):
                roi_formatted = f"{self.roi:.2f}".replace(".", "-")
                self.name = f"{self.code}-{self.period}M-R{roi_formatted}"
