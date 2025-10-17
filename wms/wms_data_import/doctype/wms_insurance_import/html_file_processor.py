from typing import Tuple
from datetime import datetime, date
from wms.wms_data_import.import_helper import create_insurance_policy, get_or_create_wms_client, get_policy_details
from wms.wms_data_import.doctype.wms_insurance_import.fields_processor import (
	process_policy_number,
	process_insurance_type,
	process_client_name,
	process_premium_amount,
	process_sum_insured_amount,
)
import frappe
from bs4 import BeautifulSoup
import pandas as pd


def get_report_duration(report_table) -> Tuple[date, date]:
	first_row_cells = [td.get_text(" ", strip=True) for td in report_table.find_all("td")]
	if not first_row_cells or "Policy Expiry Register Report" not in first_row_cells[0]:
		frappe.throw("The uploaded file is not a valid Policy Expiry Register report.")
	if len(first_row_cells) < 4 or not first_row_cells[1] or not first_row_cells[3]:
		frappe.throw("No From Date and To Date found in the report.")

	from_date = datetime.strptime(first_row_cells[1], "%d-%b-%Y").date()
	to_date = datetime.strptime(first_row_cells[3], "%d-%b-%Y").date()
	return from_date, to_date


def process_df_fields(df: pd.DataFrame) -> pd.DataFrame:
	df["Policy Number"] = df["Policy Number"].apply(process_policy_number)
	df["Policy Type"] = df["Product Code"].apply(process_insurance_type)
	df["Insured Name"] = df["Insured Name"].apply(process_client_name)
	df["Sum Insured"] = df["Sum Insured"].apply(process_sum_insured_amount)
	df["Gross Premium"] = df["Gross Premium"].apply(process_premium_amount)
	df["Policy Inception Date"] = df["Policy Inception Date"].apply(
		lambda x: datetime.strptime(x, "%d-%b-%Y").date()
	)
	df["Policy Expiry Date"] = df["Policy Expiry Date"].apply(
		lambda x: datetime.strptime(x, "%d-%b-%Y").date()
	)
	return df.drop(
		[
			"Operating Office",
			"Lob Description",
			"Lob Description",
			"Product Name",
			"Dev Officer Code",
			"Dev Officer Name",
		],
		axis=1,
	)


def validate_and_update_policy_data(app_policy_data, file_policy_data):
	if app_policy_data.start_date != file_policy_data["Policy Inception Date"]:
		app_policy_data.start_date = file_policy_data["Policy Inception Date"]
	if app_policy_data.maturity_date != file_policy_data["Policy Expiry Date"]:
		app_policy_data.maturity_date = file_policy_data["Policy Expiry Date"]


def update_client_and_policy_data(policy_table):
	headers = [td.get_text(strip=True) for td in policy_table.find("tr").find_all("td")]
	data = []
	for row in policy_table.find_all("tr")[1:]:  # skip header
		cells = [td.get_text(strip=True) for td in row.find_all("td")]
		if len(cells) == len(headers):
			data.append(cells)
	df = pd.DataFrame(data, columns=headers)
	df = df.iloc[:-1]
	df = process_df_fields(df)
	for index, file_policy_data in df.iterrows():
		policy_number = str(file_policy_data["Policy Number"])
		app_policy_data = get_policy_details(policy_number)
		if app_policy_data:
			validate_and_update_policy_data(app_policy_data, file_policy_data)
		else:
			wms_client = get_or_create_wms_client(
				"The New India Assurance Co Ltd",
				file_policy_data["Policy Holder Code"],
				file_policy_data["Insured Name"],
				file_policy_data["Insured Telephone 3"],
			)
			create_insurance_policy(file_policy_data, wms_client)
	# Check if policy exists in the system
	# If yes, validate and update detail, update client code if required
	# If no, create new policy and client as required


def process_new_india_policy_expiry_register_html(file_path):
	with open(file_path, "r", encoding="utf-8") as f:
		html_content = f.read()
		soup = BeautifulSoup(html_content, "html.parser")
		tables = soup.find_all("table")
		from_date, to_date = get_report_duration(tables[1])
		update_client_and_policy_data(tables[3])
