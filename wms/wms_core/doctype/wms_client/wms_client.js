// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS Client", {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);
            // Hide New Contact Button
            if (frm.fields_dict["contact_html"] && "contact_list" in frm.doc.__onload) {
			$()
                .find(".btn-contact").hide();
            }
        }
	},
});
