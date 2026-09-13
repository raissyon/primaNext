# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSyncRun(FrappeTestCase):
	def test_start_sets_status_and_timestamp(self):
		run = frappe.get_doc({"doctype": "Sync Run", "run_type": "Manual"}).insert()
		self.assertEqual(run.status, "Pending")
		run.start()
		self.assertEqual(run.status, "Running")
		self.assertIsNotNone(run.started_on)
		frappe.delete_doc("Sync Run", run.name)
