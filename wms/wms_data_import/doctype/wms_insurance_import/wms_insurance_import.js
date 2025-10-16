// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("WMS Insurance Import", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.upload_file) {
            if (!frm.doc.start_date && !frm.doc.error_log) {
                frm.set_value('status', "Pending");
            }
            frm.add_custom_button('Start Import', () => {
                frappe.call({
                    method: "wms.wms_data_import.doctype.wms_insurance_import.wms_insurance_import.import_insurance_policies", 
                    args: { docname: frm.doc.name },
                    freeze: true,
                    freeze_message: "Importing, please wait...",
                    callback(r) {
                        if (!r.exc) {
                            frappe.msgprint(
                                `Imported: ${r.message.imported || 0}, Updated: ${r.message.updated || 0}`
                            );
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    },
});
