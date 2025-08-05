# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSMFScheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amc: DF.Link
		amc_code: DF.Data | None
		amfi_code: DF.Data | None
		isin: DF.Data | None
		name: DF.Int | None
		nav: DF.Float
		nav_date: DF.Date | None
		option: DF.Literal["IDCW", "Growth", "Bonus"]
		plan: DF.Literal["Regular", "Direct"]
		rta: DF.Literal["CAMS", "KFintech"]
		rta_code: DF.Data | None
		scheme_name: DF.Data
		sub_option: DF.Literal[None]
		sub_type: DF.Data | None
		type: DF.Link | None
	# end: auto-generated types
	pass
