"""Post-install setup for the Primavera Integration app.

Runs once, right after `bench install-app primavera_integration`.
Creates the two integration roles (if they don't already exist) and a
disabled default Integration Settings record so the app is safe by
default: nothing runs against a real Primavera environment until an
administrator explicitly configures and enables it.
"""

import frappe


def after_install():
	_create_roles()
	_create_default_settings()


def _create_roles():
	roles = [
		"Primavera Integration Manager",
		"Primavera Integration User",
	]
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			role = frappe.new_doc("Role")
			role.role_name = role_name
			role.desk_access = 1
			role.insert(ignore_permissions=True)


def _create_default_settings():
	if frappe.db.exists("Primavera Integration Settings", "Primavera Integration Settings"):
		return

	settings = frappe.new_doc("Primavera Integration Settings")
	settings.integration_enabled = 0
	settings.integration_method = "XER"
	settings.automatic_sync_enabled = 0
	settings.sandbox_mode = 1
	settings.wbs_mapping_strategy = "Activities Only"
	settings.default_conflict_strategy = "Manual Review"
	settings.insert(ignore_permissions=True)
