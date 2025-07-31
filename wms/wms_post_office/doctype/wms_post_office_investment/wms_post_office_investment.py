# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import getdate, add_months

class WMSPostOfficeInvestment(Document):
	def before_save(self):
		if self.start_date and self.period:
			start_date = getdate(self.start_date)
			self.maturity_date = add_months(start_date, self.period) - timedelta(days=1)
