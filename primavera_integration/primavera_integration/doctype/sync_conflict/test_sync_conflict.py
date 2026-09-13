# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSyncConflict(FrappeTestCase):
	def setUp(self):
		self.run = frappe.get_doc({"doctype": "Sync Run", "run_type": "Manual"}).insert()
		self.log = frappe.get_doc(
			{
				"doctype": "Sync Log",
				"sync_run": self.run.name,
				"object_type": "Activity",
				"action": "Conflict",
				"status": "Partial Success",
			}
		).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Sync Log", self.log.name)
		frappe.delete_doc_if_exists("Sync Run", self.run.name)

	def test_resolving_stamps_user_and_time(self):
		conflict = frappe.get_doc(
			{
				"doctype": "Sync Conflict",
				"sync_log": self.log.name,
				"object_type": "Activity",
				"field_name": "planned_finish",
				"primavera_value": "2026-06-01",
				"erpnext_value": "2026-06-05",
			}
		).insert()
		conflict.resolution_status = "Resolved - P6"
		conflict.save()
		self.assertIsNotNone(conflict.resolved_on)
		self.assertEqual(conflict.resolved_by, frappe.session.user)
		frappe.delete_doc("Sync Conflict", conflict.name)
