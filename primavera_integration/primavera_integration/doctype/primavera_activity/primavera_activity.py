# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class PrimaveraActivity(Document):
	def validate(self):
		self._validate_dates()

	def _validate_dates(self):
		if self.planned_start and self.planned_finish and self.planned_start > self.planned_finish:
			frappe.throw("Planned Start cannot be after Planned Finish.")
		if self.actual_start and self.actual_finish and self.actual_start > self.actual_finish:
			frappe.throw("Actual Start cannot be after Actual Finish.")
