// Copyright (c) 2025, KNAPS and contributors
// For license information, please see license.txt

function custom_address_grid_view(frm) {
    const child_table = "WMS Client Address";  // Child DocType

    let address_grid_view = {};
    address_grid_view[child_table] = [
        {
            "fieldname": "address_1",
            "columns": 1
        },
        {
            "fieldname": "address_2",
            "columns": 2
        },
        {
            "fieldname": "address_3",
            "columns": 2
        },
        {
            "fieldname": "district",
            "columns": 1
        },
        {
            "fieldname": "city",
            "columns": 1
        },
        {
            "fieldname": "country",
            "columns": 1
        },
        {
            "fieldname": "pincode",
            "columns": 1
        }
    ];

    frappe.model.user_settings.save(frm.doctype, "GridView", address_grid_view).then((r) => {
        frappe.model.user_settings[frm.doctype] = r.message || r;

        frappe.after_ajax(() => {
            frm.fields_dict.addresses.grid.reset_grid();
            frm.fields_dict.addresses.grid.refresh();
        });

        frm.refresh_fields("addresses");
    });
}

function custom_bank_grid_view(frm) {
    const child_table = "WMS Client Bank";  // Child DocType

    let bank_grid_view = {};
    bank_grid_view[child_table] = [
        
        {
            "fieldname": "bank_name",
            "columns": 2
        },
        {
            "fieldname": "account_number",
            "columns": 2
        },
        {
            "fieldname": "type",
            "columns": 2
        },
        {
            "fieldname": "ifsc",
            "columns": 2
        },
        {
            "fieldname": "micr",
            "columns": 2
        }
    ];

    frappe.model.user_settings.save(frm.doctype, "GridView", bank_grid_view).then((r) => {
        frappe.model.user_settings[frm.doctype] = r.message || r;

        frappe.after_ajax(() => {
            frm.fields_dict.addresses.grid.reset_grid();
            frm.fields_dict.addresses.grid.refresh();
        });

        frm.refresh_fields("banks");
    });
}

frappe.ui.form.on("WMS Client", {
	refresh(frm) {
        custom_address_grid_view(frm);
        custom_bank_grid_view(frm);
	}
});