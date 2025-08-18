from frappe import _


def get_data():
	return {
		"fieldname": "client",
		"non_standard_fieldnames": {
			"WMS Service": "service_item",
			"WMS Investment Holder":"holder"
		},
		"dynamic_links": {"service_item": ["WMS Client", "service_entity"]},
		"internal_links": {
            "WMS MF Investment": ["holders", "holder"]
        },
        "internal_and_external_links": {
        },
		"transactions": [
			{"label": _("Investments"), "items": ["WMS MF Investment", "WMS PO Investment","WMS Fixed Investmentl̥"]},
			{"label": _("Insurance"), "items": ["WMS MF Investment"]}
			],
	}
