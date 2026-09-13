app_name = "primavera_integration"
app_title = "Primavera Integration"
app_publisher = "Raissyon Trading & Contracting Co."
app_description = "Primavera P6 integration for ERPNext (staging, mapping, XER import)"
app_email = "it@raissyon.com"
app_license = "mit"
app_version = "0.1.0"

# Fixtures
# ------------------
fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [["module", "=", "Primavera Integration"]],
	},
]

# Installation
# ------------------
after_install = "primavera_integration.setup.install.after_install"

# DocType Class
# ------------------
# Left empty: no core doctype class overrides in Phase 1.
override_doctype_class = {}

# Document Events
# ------------------
doc_events = {}

# Scheduled Tasks
# ------------------
# Left empty in Phase 1 — no automatic sync jobs exist yet (sync engine
# is out of scope for this phase). Populated once the sync engine ships.
scheduler_events = {}
