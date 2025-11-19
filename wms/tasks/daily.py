import frappe


def notify_role(role, message):
	# Fetch all parents (users) from Has Role
	users = frappe.get_all("Has Role", filters={"role": role}, fields=["parent"])

	# Fetch enabled System Users once
	valid_users = set(
		frappe.get_all("User", filters={"enabled": 1, "user_type": "System User"}, pluck="name")
	)

	# Filter recipients in memory
	recipients = [u.parent for u in users if u.parent in valid_users]

	# Create Notification Log (no email sent)
	for user in recipients:
		log = frappe.new_doc("Notification Log")
		log.subject = "RD Account Mismatch with PO Investment"
		log.email_content = message
		log.for_user = user
		log.type = "Alert"
		log.insert(ignore_permissions=True)

	# Real-time popup only if recipients exist
	if recipients:
		frappe.publish_realtime(
			event="show_alert",
			message={"message": message, "indicator": "red"},
			user=recipients,
			after_commit=True,
		)


def update_po_investment_in_rd_account():
	rd_accounts = frappe.get_all("WMS RD Account", filters={"po_investment": None}, pluck="name")

	for rd_account in rd_accounts:
		po_investment = frappe.db.get_value(
			"WMS PO Investment",
			{"account_number": rd_account, "scheme_code": "RD"},
			"name",
		)

		if po_investment:
			rd_doc = frappe.get_doc("WMS RD Account", rd_account)
			rd_doc.po_investment = po_investment

			try:
				rd_doc.save()
			except frappe.ValidationError as e:
				frappe.clear_last_message()
				message = f"RD Account {rd_account} and PO Investment {po_investment} " f"have {e}"
				notify_role("WMS RD Manager", message)
