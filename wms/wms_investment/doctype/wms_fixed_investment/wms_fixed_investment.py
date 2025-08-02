# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSFixedInvestment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from wms.wms_core.doctype.wms_nominee.wms_nominee import WMSNominee
		from wms.wms_investment.doctype.wms_investment_holder.wms_investment_holder import WMSInvestmentHolder

		account_number: DF.Data | None
		amount: DF.Currency
		bank: DF.Link | None
		bank_account_number: DF.Data | None
		broker_name: DF.Link | None
		cheque_date: DF.Date | None
		cheque_number: DF.Data | None
		client: DF.Link
		company: DF.Link
		currency: DF.Link | None
		entry_date: DF.Date
		holders: DF.Table[WMSInvestmentHolder]
		holding_type: DF.Link
		investment_type: DF.Literal["Cumulative", "Monthly", "Quarterly", "Half Yearly", "Yearly"]
		ledger_number: DF.Data | None
		maturity_date: DF.Date | None
		nominees: DF.Table[WMSNominee]
		period: DF.Int
		renewed_investment: DF.Link | None
		roi: DF.Float
		start_date: DF.Date | None
		status: DF.Literal["Entry Done", "Submitted", "Investment Created", "Renewed", "Matured", "Pre-Matured", "Transmitted"]
		through_broker: DF.Check
		through_us: DF.Check
	# end: auto-generated types
	pass
