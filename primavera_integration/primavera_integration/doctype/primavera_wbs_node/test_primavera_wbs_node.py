# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraWBSNode(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Primavera Project", "TEST-P6-WBS"):
			frappe.get_doc(
				{
					"doctype": "Primavera Project",
					"primavera_project_id": "TEST-P6-WBS",
					"project_name": "WBS Test Project",
				}
			).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Primavera WBS Node", "TEST-WBS-001")
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-WBS")

	def test_wbs_cannot_be_own_parent(self):
		doc = frappe.get_doc(
			{
				"doctype": "Primavera WBS Node",
				"primavera_wbs_id": "TEST-WBS-001",
				"primavera_project": "TEST-P6-WBS",
				"wbs_name": "Phase 1",
				"parent_wbs_id": "TEST-WBS-001",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)
