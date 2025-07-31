# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import getdate, add_months
import frappe
from wms.wealth_management_service.utils import get_title_fallback  # adjust path based on your app
class WMSPostOfficeInvestment(Document):
	def before_save(self):
		if self.start_date and self.period:
			start_date = getdate(self.start_date)
			self.maturity_date = add_months(start_date, self.period) - timedelta(days=1)
	
	def validate(self):
		self.validate_holder_details()

	def validate_holder_details(self):
		if self.holders and len(self.holders) > 0:

			holders = set()
			for holder in self.holders:
				if holder.holder == self.client:
					title = get_title_fallback("WMS Client", holder.holder)
					frappe.throw(f"Additional holder {title} cannot be the same as First Holder")
				if holder.holder in holders:
					title = get_title_fallback("WMS Client", holder.holder)
					frappe.throw(f"Duplicate Holder details: {title}")
				holders.add(holder.holder)
