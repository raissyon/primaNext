# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class ResourceMapping(Document):
	def validate(self):
		if not self.erpnext_employee and not self.erpnext_user:
			self.mapping_status = "Unmapped"
