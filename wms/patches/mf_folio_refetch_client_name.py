import frappe

def execute():
    null_client_name_list = frappe.get_all(
    "WMS MF Folio",
    filters={"client_name": None},
    fields=["name", "client"]
    )
    [frappe.set_value("WMS MF Folio", item['name'], "client_name", frappe.get_value("WMS Client", item['client'], "client_name")) for item in null_client_name_list]
        
