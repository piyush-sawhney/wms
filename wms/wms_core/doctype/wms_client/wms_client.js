// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS Client", {
	refresh(frm) {
        
		if (!frm.doc.__islocal) {
            frm.set_df_property("primary_email", "read_only", !!frm.doc.primary_email);
            frm.set_df_property("primary_mobile", "read_only", !!frm.doc.primary_mobile);
			frappe.contacts.render_address_and_contact(frm);
            // Hide New Contact Button
            if (frm.fields_dict["contact_html"] && "contact_list" in frm.doc.__onload) {
			$()
                .find(".btn-contact").hide();
            }
        }
	},
});
