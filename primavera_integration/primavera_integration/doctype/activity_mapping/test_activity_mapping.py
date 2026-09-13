# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestActivityMapping(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Project", "_Test Activity Mapping Project"):
			self.project = frappe.get_doc(
				{"doctype": "Project", "project_name": "_Test Activity Mapping Project"}
			).insert()
		else:
			self.project = frappe.get_doc("Project", "_Test Activity Mapping Project")

		if not frappe.db.exists("Primavera Project", "TEST-P6-AM"):
			frappe.get_doc(
				{
					"doctype": "Primavera Project",
					"primavera_project_id": "TEST-P6-AM",
					"project_name": "Activity Mapping Test",
				}
			).insert()

		if not frappe.db.exists("Primavera Activity", "TEST-AM-ACT-1"):
			frappe.get_doc(
				{
					"doctype": "Primavera Activity",
					"primavera_activity_id": "TEST-AM-ACT-1",
					"primavera_project": "TEST-P6-AM",
					"activity_name": "Excavation",
				}
			).insert()

		if not frappe.db.exists("Task", {"subject": "_Test AM Task", "project": self.project.name}):
			self.task = frappe.get_doc(
				{
					"doctype": "Task",
					"subject": "_Test AM Task",
					"project": self.project.name,
				}
			).insert()
		else:
			self.task = frappe.get_doc(
				"Task", frappe.db.get_value("Task", {"subject": "_Test AM Task"}, "name")
			)

	def tearDown(self):
		frappe.delete_doc_if_exists("Activity Mapping", "AM-TEST-AM-ACT-1")
		frappe.delete_doc_if_exists("Task", self.task.name)
		frappe.delete_doc_if_exists("Primavera Activity", "TEST-AM-ACT-1")
		frappe.delete_doc_if_exists("Primavera Project", "TEST-P6-AM")
		frappe.delete_doc_if_exists("Project", "_Test Activity Mapping Project")

	def test_activity_maps_to_exactly_one_task(self):
		mapping = frappe.get_doc(
			{
				"doctype": "Activity Mapping",
				"primavera_activity": "TEST-AM-ACT-1",
				"erpnext_task": self.task.name,
			}
		).insert()
		self.assertEqual(mapping.name, "AM-TEST-AM-ACT-1")

		duplicate = frappe.get_doc(
			{
				"doctype": "Activity Mapping",
				"primavera_activity": "TEST-AM-ACT-1",
				"erpnext_task": self.task.name,
			}
		)
		self.assertRaises(frappe.DuplicateEntryError, duplicate.insert)
		frappe.delete_doc("Activity Mapping", mapping.name)
