# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraProject(FrappeTestCase):
	def test_primavera_project_id_is_unique(self):
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-001")
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Project",
				"primavera_project_id": "TEST-P6-001",
				"project_name": "Test Project One",
			}
		).insert()
		self.assertEqual(doc.name, "TEST-P6-001")

		duplicate = frappe.get_doc(
			{
				"doctype": "Primavera Project",
				"primavera_project_id": "TEST-P6-001",
				"project_name": "Duplicate Attempt",
			}
		)
		self.assertRaises(frappe.DuplicateEntryError, duplicate.insert)
		frappe.delete_doc("Primavera Project", "TEST-P6-001")
