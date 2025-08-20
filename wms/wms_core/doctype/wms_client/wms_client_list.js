frappe.listview_settings["WMS Client"] = {
	add_fields: ["client_name", "pan", "primary_mobile", "primary_email", "classification","client_group"],
    hide_name_column: true, // hide the last column which shows the `name`
    hide_name_filter: true,
    total_fields: 9 // hide the default filter field for the name column
};
