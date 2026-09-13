# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class PrimaveraWBSNode(Document):
	def validate(self):
		self._validate_parent_not_self()

	def _validate_parent_not_self(self):
		if self.parent_wbs_id and self.parent_wbs_id == self.primavera_wbs_id:
			frappe.throw("A WBS node cannot be its own parent.")
