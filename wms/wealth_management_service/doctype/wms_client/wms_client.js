// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS Client", {
	type(frm) {
        doc = frm.doc;
        frm.toggle_display(['sub_type'], ['Individual', 'Company'].includes(doc.type) );
        switch (doc.type) {
            case "Individual":
                frm.set_value("sub_type", 'Resident');
                frm.set_df_property("sub_type", "options", ['Resident', 'Minor', 'NRI']);
                break;
            case "Company":
                frm.set_value("sub_type", 'Private Limted');
                frm.set_df_property("sub_type", "options", ['Public Limited', 'Private Limted']);
                break;
        }
	},
});
