from frappe import _


def get_data():
	return {
		"fieldname": "client",
		"non_standard_fieldnames": {
			"WMS Service": "service_item",
			"WMS Family": "family_head"
		},
		"dynamic_links": {"service_item": ["WMS Client", "service_entity"]},
		"internal_links": {

        },
        "internal_and_external_links": {
			
        },
		"transactions": [
			{"label": _("Investments"), "items": ["WMS MF Investment","WMS Fixed Investment","WMS PO Investment","WMS Demat Account"]},
			{"label": _("Insurance"), "items": ["WMS Insurance Policy"]},
			{"label": _("Family"), "items": ["WMS Family"]},
			{"label": _("Service Requests"), "items": ["WMS Service"]},
			{"label": _("Banks"), "items": ["WMS Bank"]}
			],
	}
