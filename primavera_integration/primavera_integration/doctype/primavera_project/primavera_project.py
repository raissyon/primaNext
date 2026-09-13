# Copyright (c) 2026, Raissyon Trading & Contracting Co.

from frappe.model.document import Document


class PrimaveraProject(Document):
	"""Read-mostly staging mirror of a Primavera P6 project. This record is
	written by the (future) parser/sync engine, not edited by hand — it
	exists so ERPNext has a normalized, queryable copy of what the last
	XER/XML/API fetch contained, independent of which adapter produced it.
	"""

	def before_save(self):
		# Staging records are allowed to be re-imported repeatedly; treat
		# any manual edit to erpnext_project as authoritative only if it
		# doesn't already conflict with an existing Project Mapping.
		self._guard_against_duplicate_mapping()

	def _guard_against_duplicate_mapping(self):
		import frappe

		if not self.erpnext_project:
			return
		existing = frappe.db.get_value(
			"Project Mapping",
			{"primavera_project": self.name, "erpnext_project": ["!=", self.erpnext_project]},
			"name",
		)
		if existing:
			frappe.throw(
				f"This Primavera Project is already mapped to a different ERPNext "
				f"Project via Project Mapping {existing}."
			)
