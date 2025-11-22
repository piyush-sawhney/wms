import frappe


def execute():
	contact_phone_list = frappe.get_all("Contact Phone", pluck="name")
	for contact_phone in contact_phone_list:
		contact_phone_doc = frappe.get_doc("Contact Phone", contact_phone)
		wms_phone_number_doc = frappe.new_doc("WMS Phone Number")
		wms_phone_number_doc.parent = contact_phone_doc.parent
		wms_phone_number_doc.parenttype = "WMS Client"
		wms_phone_number_doc.parentfield = "phone_numbers"
		wms_phone_number_doc.phone = f"+91-{contact_phone_doc.phone}"
		wms_phone_number_doc.is_primary_phone = contact_phone_doc.is_primary_mobile_no
		if contact_phone_doc.is_primary_mobile_no:
			wms_phone_number_doc.is_primary_whatsapp = 1

		try:
			wms_phone_number_doc.save(ignore_permissions=True)
		except Exception as e:
			frappe.log_error(f"Failed to migrate Contact Phone {contact_phone}: {e}")
	frappe.clear_cache(doctype="WMS Client")
	client_list = frappe.get_all("WMS Client", pluck="name")
	for client in client_list:
		client_doc = frappe.get_doc("WMS Client", client)
		if client_doc.phone_numbers:
			primary_phones = [phone for phone in client_doc.phone_numbers if phone.is_primary_phone]
			if primary_phones:
				client_doc.primary_mobile = primary_phones[0].phone
				try:
					client_doc.save(ignore_permissions=True)
				except Exception as e:
					frappe.log_error(f"Failed to update WMS Client {client}: {e}")
