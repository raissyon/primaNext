# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SyncRun(Document):
	def start(self):
		self.status = "Running"
		self.started_on = now_datetime()
		self.save(ignore_permissions=True)

	def finish(self):
		"""Recompute status from the Sync Log rows attached to this run and
		stamp the end time. Called by the (future) sync engine once every
		batch has been processed."""
		total = frappe.db.count("Sync Log", {"sync_run": self.name})
		success = frappe.db.count("Sync Log", {"sync_run": self.name, "status": "Success"})
		failed = frappe.db.count("Sync Log", {"sync_run": self.name, "status": "Failed"})
		conflicts = frappe.db.count(
			"Sync Conflict", {"sync_log": ["in", frappe.get_all(
				"Sync Log", filters={"sync_run": self.name}, pluck="name"
			)]}
		)

		self.total_objects = total
		self.success_count = success
		self.failed_count = failed
		self.conflict_count = conflicts
		self.ended_on = now_datetime()

		if failed == 0:
			self.status = "Success"
		elif success > 0:
			self.status = "Partial Success"
		else:
			self.status = "Failed"

		self.save(ignore_permissions=True)
