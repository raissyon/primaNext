# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestProjectMapping(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Primavera Project", "TEST-P6-MAP1"):
			frappe.get_doc(
				{
					"doctype": "Primavera Project",
					"primavera_project_id": "TEST-P6-MAP1",
					"project_name": "Mapping Test 1",
				}
			).insert()
		if not frappe.db.exists("Primavera Project", "TEST-P6-MAP2"):
			frappe.get_doc(
				{
					"doctype": "Primavera Project",
					"primavera_project_id": "TEST-P6-MAP2",
					"project_name": "Mapping Test 2",
				}
			).insert()
		if not frappe.db.exists("Project", "_Test Mapping Project"):
			frappe.get_doc(
				{"doctype": "Project", "project_name": "_Test Mapping Project"}
			).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Project Mapping", f"PM-TEST-P6-MAP1")
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-MAP1")
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-MAP2")
		frappe.delete_doc_if_exists("Project", "_Test Mapping Project")

	def test_same_erpnext_project_cannot_be_mapped_twice(self):
		project_name = frappe.db.get_value(
			"Project", {"project_name": "_Test Mapping Project"}, "name"
		)
		first = frappe.get_doc(
			{
				"doctype": "Project Mapping",
				"primavera_project": "TEST-P6-MAP1",
				"erpnext_project": project_name,
			}
		).insert()

		second = frappe.get_doc(
			{
				"doctype": "Project Mapping",
				"primavera_project": "TEST-P6-MAP2",
				"erpnext_project": project_name,
			}
		)
		self.assertRaises(frappe.ValidationError, second.insert)
		frappe.delete_doc("Project Mapping", first.name)
