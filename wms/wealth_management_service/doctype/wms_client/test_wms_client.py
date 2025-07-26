# Copyright (c) 2025, KNAPS and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

def create_test_data():
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
 		"doctype": "Contact",
 		"first_name": "Test Client 1" 
		}).insert()
	
	doc = frappe.get_doc({
 		"doctype": "WMS Client",
 		"client_name": "Test Client 1",
		"client_details": "Test Client 1"
		}).insert()
	



class TestWMSClient(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		create_test_data()
	

	def test_client_creation(self):
		client = frappe.get_last_doc("WMS Client")
		self.assertEqual(client.type, "Individual")
		self.assertEqual(client.client_name, "Test Client 1")