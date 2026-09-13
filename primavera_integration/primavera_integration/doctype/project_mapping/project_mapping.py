# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class ProjectMapping(Document):
	def validate(self):
		self._prevent_duplicate_mapping()

	def _prevent_duplicate_mapping(self):
		"""Belt-and-braces on top of the unique index: give a readable
		error instead of a raw DB duplicate-key exception, and catch the
		cross-field case (same ERPNext Project mapped from two different
		Primavera Projects) that a single-column unique index can't."""
		existing_for_erpnext_project = frappe.db.get_value(
			"Project Mapping",
			{"erpnext_project": self.erpnext_project, "name": ["!=", self.name]},
			"name",
		)
		if existing_for_erpnext_project:
			frappe.throw(
				f"ERPNext Project {self.erpnext_project} is already linked to a "
				f"different Primavera Project via {existing_for_erpnext_project}."
			)

	def on_update(self):
		frappe.db.set_value(
			"Primavera Project", self.primavera_project, "erpnext_project", self.erpnext_project
		)
