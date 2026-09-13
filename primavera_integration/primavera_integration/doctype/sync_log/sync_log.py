# Copyright (c) 2026, Raissyon Trading & Contracting Co.

import json

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

SECRET_KEYS = ("password", "token", "secret", "credentials_reference", "authorization")


class SyncLog(Document):
	def before_insert(self):
		if not self.timestamp:
			self.timestamp = now_datetime()
		self.request_payload = self._redact(self.request_payload)
		self.response_payload = self._redact(self.response_payload)

	@staticmethod
	def _redact(payload):
		"""Never let credentials/tokens make it into a Sync Log, even if a
		caller passes them in by mistake."""
		if not payload:
			return payload
		try:
			data = json.loads(payload) if isinstance(payload, str) else payload
		except (TypeError, ValueError):
			return payload

		def scrub(obj):
			if isinstance(obj, dict):
				return {
					k: ("***REDACTED***" if any(s in k.lower() for s in SECRET_KEYS) else scrub(v))
					for k, v in obj.items()
				}
			if isinstance(obj, list):
				return [scrub(v) for v in obj]
			return obj

		return frappe.as_json(scrub(data))
