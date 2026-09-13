# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPrimaveraIntegrationSettings(FrappeTestCase):
	def test_singleton_loads_with_safe_defaults(self):
		settings = frappe.get_single("Primavera Integration Settings")
		self.assertEqual(settings.doctype, "Primavera Integration Settings")
		# Whatever an environment has configured, automatic sync must never
		# silently default to "on" for a freshly installed site.
		if not frappe.db.get_value(
			"Primavera Integration Settings", None, "modified_by"
		):
			self.assertFalse(settings.automatic_sync_enabled)

	def test_api_validation_requires_endpoint(self):
		settings = frappe.get_single("Primavera Integration Settings")
		settings.integration_method = "API"
		settings.automatic_sync_enabled = 1
		settings.primavera_endpoint = None
		self.assertRaises(frappe.ValidationError, settings.validate)
