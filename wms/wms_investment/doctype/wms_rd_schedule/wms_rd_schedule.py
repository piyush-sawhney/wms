# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSRDSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from wms.wms_investment.doctype.wms_rd_transaction.wms_rd_transaction import WMSRDTransaction

		amended_from: DF.Link | None
		deposit_amount: DF.Float
		rd_accounts: DF.Table[WMSRDTransaction]
		schedule_amount: DF.Float
		schedule_date: DF.Date | None
		schedule_number: DF.Data | None
		schedule_type: DF.Literal["Cash", "Cheque"]
		total_rebate: DF.Float
		total_surcharge: DF.Float
	# end: auto-generated types
	pass
