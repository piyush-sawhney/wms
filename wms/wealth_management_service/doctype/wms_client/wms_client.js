// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt


const set_dob_pob = (frm,type)=>{
    if (type == "Individual") {
        frm.set_df_property("dob", "label", "Date of Birth");
        frm.set_df_property("pob", "label", "Place of Birth");
    }
    else   {
        frm.set_df_property("dob", "label", "Date of Incorporation");
        frm.set_df_property("pob", "label", "Place of Incorporation");
    }

}

frappe.ui.form.on("WMS Client", {
	type(frm) {
        doc = frm.doc;
        frm.toggle_display(['sub_type'], ['Individual', 'Company'].includes(doc.type) );
        switch (doc.type) {
            case "Individual":
                frm.set_value("sub_type", 'Resident');
                frm.set_df_property("sub_type", "options", ['Resident', 'Minor', 'NRI']);
                set_dob_pob(frm,doc.type)
                break;
            case "Company":
                frm.set_value("sub_type", 'Private Limted');
                frm.set_df_property("sub_type", "options", ['Public Limited', 'Private Limted']);
                set_dob_pob(frm,doc.type)
                break;
            default:
                set_dob_pob(frm,doc.type)
                break;
        }
	},
    before_save(frm){
        doc = frm.doc;
        if (doc.pan) {
            doc.pan = doc.pan.toUpperCase()
        }
    }
});
