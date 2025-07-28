# Copyright (c) 2025, KNAPS and Contributors
# See license.txt

import frappe
import random
import string
from frappe.tests.utils import FrappeTestCase
from datetime import datetime, timedelta

def random_dob(min_age=18, max_age=65):
    today = datetime.today()
    start_date = today.replace(year=today.year - max_age)
    end_date = today.replace(year=today.year - min_age)
    
    random_days = random.randint(0, (end_date - start_date).days)
    dob = start_date + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")

def random_dob_under_18():
    today = datetime.today()
    max_birth_date = today.replace(year=today.year - 1)
    min_birth_date = today.replace(year=today.year - 18)

    random_days = random.randint(0, (max_birth_date - min_birth_date).days)
    dob = min_birth_date + timedelta(days=random_days)

    return dob.strftime("%Y-%m-%d")
def random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    domain_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
    tlds = [".com", ".in", ".org", ".net", ".co.in", ".biz", ".io"]
    domain_extension = random.choice(tlds)
    
    return f"{username}@{domain_name}{domain_extension}"
test_pan_data ={
            "doctype": "WMS PAN",
            "pan": "ACCPS1234F",
}

test_bank_data = [
	{
            "doctype": "WMS Bank",
            "account_number": str(random.randint(10**15, 10**16 - 1)),
            "ifsc": ''.join(random.choices(string.digits, k=10)),
            "micr": str(random.randint(10**8, 10**9 - 1)),
            "type": "Savings",
            "name1": ''.join(random.choices(string.digits, k=10))
    }
]
test_address_data = [
	{
            "doctype": "WMS Address",
            "address_title": ''.join(random.choices(string.ascii_letters + string.digits, k=50)),
            "address_1": ''.join(random.choices(string.ascii_letters + string.digits, k=50)),
            "address_2": ''.join(random.choices(string.ascii_letters + string.digits, k=50)),
            "address_3": ''.join(random.choices(string.ascii_letters + string.digits, k=50)),
            "district": ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
            "city": ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
            "state": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "pincode": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "country": "India"
    }
]

test_email_ids = [
                {
                    "doctype": "Contact Email",
                    "email_id": random_email(),
                    "is_primary": 1
                }
]
test_phone_numbers = [
                {
                    "doctype": "Contact Phone",
                    "phone": str(random.randint(10**9, 10**10 - 1)),
                    "is_primary_phone": 1
                }
]
test_data = {
	"doctype": "WMS Client",
    "client_name": ''.join(random.choices(string.ascii_letters + string.digits, k=30)),
    "classification": "Resident",
    "pan": test_pan_data["pan"],
    "dob": random_dob(),
    "pob": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
    "email_ids": test_email_ids,
    "phone_numbers": test_phone_numbers,
    "addresses": [
        {
            "doctype": "WMS Client Address",
            "address_title": test_address_data[0]["address_title"]
        }
    ]
    ,
    "banks": [
        {
            "doctype": "WMS Client Bank",
            "account_number": test_bank_data[0]["account_number"]
        }
    ]       
}

	



class TestWMSClient(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		
		frappe.get_doc(test_pan_data).insert()
		frappe.get_doc(test_bank_data[0]).insert()
		frappe.get_doc(test_address_data[0]).insert()


	def test_resident_client_creation(self):
		client = frappe.get_doc(test_data).insert()
		self.assertEqual(client.type, "Individual")
		self.assertEqual(client.client_name, test_data["client_name"])
		self.assertEqual(client.pan, test_data["pan"])
		self.assertEqual(client.dob, test_data["dob"])
		self.assertEqual(client.pob, test_data["pob"])
		for index,item in enumerate(client.email_ids):
			self.assertEqual(item.email_id, test_data["email_ids"][index]["email_id"])
		for index,item in enumerate(client.phone_numbers):
			self.assertEqual(item.phone, test_data["phone_numbers"][index]["phone"])
		for index,item in enumerate(client.addresses):
			self.assertEqual(item.address_title, test_data["addresses"][index]["address_title"])
		for index,item in enumerate(client.banks):
			self.assertEqual(item.account_number, test_data["banks"][index]["account_number"])

	def test_minor_client_creation_with_age_less_than_18(self):
		test_minor_data = {
			"doctype": "WMS Client",
            "client_name": ''.join(random.choices(string.ascii_letters + string.digits, k=30)),
            "classification": "Minor",
            "dob": random_dob_under_18()
        }
		
		client = frappe.get_doc(test_minor_data).insert()
		self.assertEqual(client.type, "Individual")
		self.assertEqual(client.client_name, test_minor_data["client_name"])
		self.assertEqual(client.dob, test_minor_data["dob"])

	def test_resident_client_creation_with_age_less_than_18(self):
		test_resident_data = {
			"doctype": "WMS Client",
            "client_name": ''.join(random.choices(string.ascii_letters + string.digits, k=30)),
            "classification": "Resident",
            "dob": random_dob_under_18()
        }
		
		client = frappe.get_doc(test_resident_data).insert()
		self.assertEqual(client.type, "Individual")
		self.assertEqual(client.classification, "Minor")
		self.assertEqual(client.client_name, test_resident_data["client_name"])
		self.assertEqual(client.dob, test_resident_data["dob"])
		