# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraImport(FrappeTestCase):
	def test_existing_project_mode_requires_target_project(self):
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Import",
				"xer_file": "/files/test.xer",
				"project_mode": "Existing Project",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_new_project_mode_requires_name(self):
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Import",
				"xer_file": "/files/test.xer",
				"project_mode": "Create New Project",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_valid_new_project_mode_inserts(self):
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Import",
				"xer_file": "/files/test.xer",
				"project_mode": "Create New Project",
				"new_project_name": "Test New Project From XER",
			}
		).insert()
		self.assertEqual(doc.status, "Uploaded")
		self.assertEqual(doc.imported_by, frappe.session.user)
		frappe.delete_doc("Primavera Import", doc.name)
