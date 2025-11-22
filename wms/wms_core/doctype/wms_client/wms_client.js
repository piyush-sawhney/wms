// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS Client", {
	is_whatsapp_no(frm) {
		if (frm.doc.is_whatsapp_no) {
			frm.set_df_property("whatsapp_number", "read_only", true);
		} else {
			frm.set_df_property("whatsapp_number", "read_only", false);
		}
	},
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frm.set_df_property("primary_email", "read_only", !!frm.doc.primary_email);
			frm.set_df_property("primary_mobile", "read_only", !!frm.doc.primary_mobile);
			frm.set_df_property("whatsapp_number", "read_only", !!frm.doc.whatsapp_number);
			frm.set_df_property("is_whatsapp_no", "read_only", !!frm.doc.whatsapp_number);

			frappe.contacts.render_address_and_contact(frm);
			// Hide New Contact Button
			if (frm.fields_dict["contact_html"] && "contact_list" in frm.doc.__onload) {
				$().find(".btn-contact").hide();
			}
		} else {
			frm.set_df_property("whatsapp_number", "read_only", true);
		}
	},
});
