# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.model.document import Document


class PrimaveraIntegrationSettings(Document):
	def validate(self):
		self._validate_api_fields()

	def _validate_api_fields(self):
		"""API-specific fields are only meaningful when the API adapter is
		selected. We don't require them yet (the APIAdapter isn't built in
		this phase) but we do stop obviously inconsistent configuration."""
		if self.integration_method == "API" and self.automatic_sync_enabled:
			if not self.primavera_endpoint:
				frappe.throw(
					"Primavera Endpoint URL is required before enabling automatic "
					"synchronization with Integration Method = API."
				)

	def get_credentials(self):
		"""Server-side only accessor. Never call this from client scripts
		or include its return value in anything that gets logged."""
		frappe.only_for(("System Manager", "Primavera Integration Manager"))
		return self.get_password("credentials_reference", raise_exception=False)
