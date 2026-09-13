# Copyright (c) 2026, Raissyon Trading & Contracting Co.

"""Background-job entry point for parsing an uploaded XER file.

This module is deliberately the ONLY integration point between the
'Primavera Import' UI/DocType and the XER parser: the Primavera Import
doctype calls `queue_parse()`, which enqueues `run_parse_job` here. This
keeps the doctype and the Page free of any parsing logic, so wiring in the
real parser (Phase 2) means changing this one function's body, not the
schema or the UI.

The actual XER table parsing, staging-record upserts, and preview
generation are out of scope for this phase (see the approved architecture
and delivery plan). Until they exist, this job records that parsing was
requested and leaves the Primavera Import record in a clear, honest state
rather than pretending to have parsed anything.
"""

import frappe
from frappe.utils import now_datetime


def run_parse_job(import_name: str):
	doc = frappe.get_doc("Primavera Import", import_name)
	try:
		_run(doc)
	except Exception:
		doc.reload()
		doc.status = "Failed"
		doc.error_message = frappe.get_traceback()
		doc.save(ignore_permissions=True)
		frappe.log_error(
			title=f"Primavera Import parse failed: {import_name}",
			message=frappe.get_traceback(),
		)
		raise


def _run(doc):
	# Phase boundary: the XER parser (adapters.xer_adapter.XERAdapter) and
	# the staging upsert / preview-generation logic land in the Sync Engine
	# phase. Recording this explicitly on the document — rather than
	# silently marking it "Parsed" — keeps the audit trail honest about
	# what actually happened to this file.
	doc.reload()
	doc.status = "Uploaded"
	doc.error_message = (
		"XER parsing is not yet available in this installation "
		f"(requested at {now_datetime()}). This phase ships the data "
		"model and UI foundation only; the parser lands in the next "
		"release."
	)
	doc.save(ignore_permissions=True)
