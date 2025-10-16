import frappe
def update_insurance_policy_if_required(policy_data):
    pass

def get_or_create_wms_client(client_code_provider, client_code, client_name=None, mobile_no=None):
    wms_client = frappe.get_value(
        "WMS Client Codes",
        {
            "company_name": client_code_provider, "code": client_code
        },
        "parent"
    )
    if not wms_client:
        wms_client = frappe.get_doc({
            "doctype": "WMS Client",
            "client_name": client_name,
            "codes": [
                {"company_name": client_code_provider, "code": client_code}
            ]
        })
        wms_client.insert(ignore_permissions=True)
    return wms_client