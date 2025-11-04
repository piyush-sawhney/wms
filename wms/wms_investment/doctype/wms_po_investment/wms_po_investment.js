// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS PO Investment", {
	client(frm) {
		frm.set_value("guardian", null);

		if (frm.doc.client_classification === "Minor") {
			frm.toggle_display("guardian", true);
		} else {
			frm.toggle_display("guardian", false);
		}
	},

	guardian(frm) {
		if (frm.doc.guardian === frm.doc.client) {
			frm.set_value("guardian", null);
		}
	},
});
