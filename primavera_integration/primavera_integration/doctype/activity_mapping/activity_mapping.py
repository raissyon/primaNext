# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class ActivityMapping(Document):
	def validate(self):
		self._auto_fill_project_mapping()
		self._prevent_cross_project_task()

	def _auto_fill_project_mapping(self):
		if self.project_mapping:
			return
		primavera_project = frappe.db.get_value(
			"Primavera Activity", self.primavera_activity, "primavera_project"
		)
		if primavera_project:
			self.project_mapping = frappe.db.get_value(
				"Project Mapping", {"primavera_project": primavera_project}, "name"
			)

	def _prevent_cross_project_task(self):
		"""The Primavera Activity ID is the durable identifier — never the
		Task subject/name — so this check is what actually stops a Task
		belonging to Project A from being mapped to an Activity that lives
		under a Primavera Project mapped to Project B."""
		if not self.project_mapping:
			return
		mapped_erpnext_project = frappe.db.get_value(
			"Project Mapping", self.project_mapping, "erpnext_project"
		)
		task_project = frappe.db.get_value("Task", self.erpnext_task, "project")
		if mapped_erpnext_project and task_project and mapped_erpnext_project != task_project:
			frappe.throw(
				f"Task {self.erpnext_task} belongs to Project {task_project}, but this "
				f"Primavera Activity's Project Mapping points to {mapped_erpnext_project}."
			)
