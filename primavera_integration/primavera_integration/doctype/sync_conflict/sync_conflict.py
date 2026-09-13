# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SyncConflict(Document):
	def before_save(self):
		if self.resolution_status != "Open" and not self.resolved_on:
			self.resolved_by = frappe.session.user
			self.resolved_on = now_datetime()
