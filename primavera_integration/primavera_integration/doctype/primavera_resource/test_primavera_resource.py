# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraResource(FrappeTestCase):
	def test_create_and_delete(self):
		frappe.delete_doc_if_exists("Primavera Resource", "TEST-RES-001")
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Resource",
				"primavera_resource_id": "TEST-RES-001",
				"resource_name": "Site Electrician",
				"resource_type": "Labor",
			}
		).insert()
		self.assertEqual(doc.name, "TEST-RES-001")
		frappe.delete_doc("Primavera Resource", "TEST-RES-001")
