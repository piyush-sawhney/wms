import frappe

def execute():
    null_client_name_list = frappe.get_all(
    "WMS MF Transaction",
    filters={"client_name": None},
    fields=["name", "folio_number"]
    )
    [frappe.set_value("WMS MF Transaction", item["name"], "client_name", frappe.get_value("WMS MF Folio", item['folio_number'], "client_name")) for item in null_client_name_list]
        
