from typing import Tuple
from datetime import datetime, date
import frappe
from bs4 import BeautifulSoup
import pandas as pd
def get_report_duration(report_table) -> Tuple[date,date]:
	first_row_cells = [td.get_text(" ", strip=True) for td in report_table.find_all("td")]
	if not first_row_cells or 'Policy Expiry Register Report' not in first_row_cells[0]:
		frappe.throw("The uploaded file is not a valid Policy Expiry Register report.")
	if len(first_row_cells) < 4 or not first_row_cells[1] or not first_row_cells[3]:
		frappe.throw("No From Date and To Date found in the report.")
		
	from_date = datetime.strptime(first_row_cells[1], "%d-%b-%Y").date()
	to_date = datetime.strptime(first_row_cells[3], "%d-%b-%Y").date()
	return from_date, to_date

def update_client_and_policy_data(policy_table):
	headers = [td.get_text(strip=True) for td in policy_table.find("tr").find_all("td")]
	data = []
	for row in policy_table.find_all("tr")[1:]:  # skip header
		cells = [td.get_text(strip=True) for td in row.find_all("td")]
		if len(cells) == len(headers):
			data.append(cells)
	df = pd.DataFrame(data, columns=headers)
	print(df)

def process_new_india_policy_expiry_register_html(file_path):
	with open(file_path, "r", encoding="utf-8") as f:
		html_content = f.read()
		soup = BeautifulSoup(html_content, "html.parser")
		tables = soup.find_all("table")
		from_date, to_date = get_report_duration(tables[1])
		update_client_and_policy_data(tables[3])
