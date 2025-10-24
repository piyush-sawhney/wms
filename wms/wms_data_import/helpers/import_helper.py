import frappe

from wms.wms_data_import.helpers.import_logger import log_error, log_success


def get_or_create_wms_client(dt, client_code_provider, client_code, client_name=None, mobile_no=None):
	wms_client = frappe.get_value(
		"WMS Client Codes",
		{"company_name": client_code_provider, "code": client_code},
		"parent",
	)
	if not wms_client:
		try:
			wms_client = frappe.get_doc(
				{
					"doctype": "WMS Client",
					"client_name": client_name,
					"primary_mobile_no": mobile_no,
					"codes": [{"company_name": client_code_provider, "code": client_code}],
				}
			)
			wms_client.insert(ignore_permissions=True)
			message = f"Client {client_name} created successfully."
			log_success(dt, message, commit=True)
		except Exception:
			message = f"Client {client_name} creation failed."
			log_error(dt, message, commit=True)
			raise
	return wms_client


def get_policy_details_from_web(policy_number: str):
	policy = frappe.db.exists("WMS Insurance Policy", {"policy_number": policy_number})
	if policy:
		return frappe.get_doc("WMS Insurance Policy", {"policy_number": policy_number})
	else:
		return policy


def create_insurance_policy(dt, policy_data, wms_client):
	policy_period_months = frappe.utils.month_diff(
		policy_data["Policy Expiry Date"], policy_data["Policy Inception Date"]
	)
	try:
		policy = frappe.get_doc(
			{
				"doctype": "WMS Insurance Policy",
				"policy_number": policy_data["Policy Number"],
				"insurance_type": policy_data["Policy Type"],
				"proposer": wms_client,
				"start_date": policy_data["Policy Inception Date"],
				"maturity_date": policy_data["Policy Expiry Date"],
				"sum_assured": policy_data["Sum Insured"],
				"premium": policy_data["Gross Premium"],
				"is_existing_policy": True,
				"period_type": "Months",
				"period": policy_period_months,
				"provider": "The New India Assurance Co Ltd",
				"desciption": policy_data["Policy Type"],
			}
		)
		if policy_data["Policy Expiry Date"] > frappe.utils.getdate(frappe.utils.today()):
			policy.status = "Active"
		else:
			policy.status = "Expired"
		if policy_data["Policy Type"] == "Vehicle Insurance":
			policy.vehicle_number = policy_data["Registration No"]
			policy.chassis_number = policy_data["Chassis No"]
			policy.engine_number = policy_data["Engine No"]
		policy.insert(ignore_permissions=True)
		message = (
			f"Policy {policy_data['Policy Number']} for client {wms_client.get_title()} created successfully."
		)
		log_success(dt, message, commit=True)
	except Exception:
		message = (
			f"Policy {policy_data['Policy Number']} for client {wms_client.get_title()} creation failed."
		)
		log_error(dt, message, commit=True)
		return policy
