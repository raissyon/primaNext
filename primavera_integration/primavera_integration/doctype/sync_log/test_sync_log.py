# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import json

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSyncLog(FrappeTestCase):
	def setUp(self):
		self.run = frappe.get_doc({"doctype": "Sync Run", "run_type": "Manual"}).insert()

	def tearDown(self):
		frappe.delete_doc_if_exists("Sync Run", self.run.name)

	def test_credentials_are_redacted(self):
		log = frappe.get_doc(
			{
				"doctype": "Sync Log",
				"sync_run": self.run.name,
				"object_type": "Project",
				"action": "Created",
				"status": "Success",
				"request_payload": json.dumps({"endpoint": "x", "token": "super-secret"}),
			}
		).insert()
		saved = json.loads(log.request_payload)
		self.assertEqual(saved["token"], "***REDACTED***")
		self.assertEqual(saved["endpoint"], "x")
		frappe.delete_doc("Sync Log", log.name)
