# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraActivity(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Primavera Project", "TEST-P6-ACT"):
			frappe.get_doc(
				{
					"doctype": "Primavera Project",
					"primavera_project_id": "TEST-P6-ACT",
					"project_name": "Activity Test Project",
				}
			).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Primavera Activity", "TEST-ACT-001")
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-ACT")

	def test_planned_start_after_finish_is_rejected(self):
		doc = frappe.get_doc(
			{
				"doctype": "Primavera Activity",
				"primavera_activity_id": "TEST-ACT-001",
				"primavera_project": "TEST-P6-ACT",
				"activity_name": "Pour Foundation",
				"planned_start": "2026-05-10",
				"planned_finish": "2026-05-01",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)
