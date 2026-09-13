# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class PrimaveraImport(Document):
	def before_insert(self):
		if not self.import_date:
			self.import_date = now_datetime()
		if not self.imported_by:
			self.imported_by = frappe.session.user
		self.file_url = self.xer_file

	def validate(self):
		self._validate_project_mode_fields()
		self._validate_not_already_mapped_to_a_different_project()

	def _validate_project_mode_fields(self):
		if self.project_mode == "Existing Project" and not self.target_erpnext_project:
			frappe.throw("Select a Target ERPNext Project, or switch to Create New Project.")
		if self.project_mode == "Create New Project" and not self.new_project_name:
			frappe.throw("Enter a name for the new ERPNext Project.")

	def _validate_not_already_mapped_to_a_different_project(self):
		if self.project_mode != "Existing Project" or not self.selected_primavera_project:
			return
		existing_mapping = frappe.db.get_value(
			"Project Mapping", {"primavera_project": self.selected_primavera_project}, "erpnext_project"
		)
		if existing_mapping and existing_mapping != self.target_erpnext_project:
			frappe.throw(
				f"Primavera Project {self.selected_primavera_project} is already mapped to "
				f"ERPNext Project {existing_mapping}. Select that project, or create the "
				f"mapping change from Project Mapping directly."
			)

	@frappe.whitelist()
	def queue_parse(self):
		"""Enqueue the (future) XER parser as a background job. Kept as a
		single, narrow entry point now so the Primavera Import Page and any
		other caller has one stable API to call once the parser ships —
		nothing about this doctype's schema needs to change when it does.
		"""
		frappe.only_for(("System Manager", "Primavera Integration Manager", "Primavera Integration User"))
		self.status = "Parsing"
		self.save()
		frappe.enqueue(
			"primavera_integration.tasks.parse_import.run_parse_job",
			queue="long",
			import_name=self.name,
		)
		return {"status": self.status}
