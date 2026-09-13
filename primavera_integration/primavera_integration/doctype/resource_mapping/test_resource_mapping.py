# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestResourceMapping(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Primavera Resource", "TEST-RM-RES-1"):
			frappe.get_doc(
				{
					"doctype": "Primavera Resource",
					"primavera_resource_id": "TEST-RM-RES-1",
					"resource_name": "Test Resource",
				}
			).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Resource Mapping", "RM-TEST-RM-RES-1")
		frappe.delete_doc_if_exists("Primavera Resource", "TEST-RM-RES-1")

	def test_unmapped_status_when_no_target_given(self):
		doc = frappe.get_doc(
			{
				"doctype": "Resource Mapping",
				"primavera_resource": "TEST-RM-RES-1",
			}
		).insert()
		self.assertEqual(doc.mapping_status, "Unmapped")
