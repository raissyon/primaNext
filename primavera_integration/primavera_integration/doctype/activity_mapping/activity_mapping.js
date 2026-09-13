// Copyright (c) 2026, Raissyon Trading & Contracting Co.

frappe.ui.form.on("Activity Mapping", {
	primavera_activity: function (frm) {
		if (!frm.doc.primavera_activity) {
			return;
		}
		frappe.db.get_value(
			"Primavera Activity",
			frm.doc.primavera_activity,
			"primavera_project",
			(r) => {
				if (!r || !r.primavera_project) {
					return;
				}
				frappe.db.get_value(
					"Project Mapping",
					{ primavera_project: r.primavera_project },
					"name",
					(mapping) => {
						if (mapping && mapping.name) {
							frm.set_value("project_mapping", mapping.name);
						}
					}
				);
			}
		);
	},

	project_mapping: function (frm) {
		// Once a Project Mapping is chosen, only offer Tasks that belong
		// to that mapping's ERPNext Project when picking erpnext_task.
		if (!frm.doc.project_mapping) {
			frm.set_query("erpnext_task", () => ({ filters: {} }));
			return;
		}
		frappe.db.get_value(
			"Project Mapping",
			frm.doc.project_mapping,
			"erpnext_project",
			(r) => {
				if (r && r.erpnext_project) {
					frm.set_query("erpnext_task", () => ({
						filters: { project: r.erpnext_project },
					}));
				}
			}
		);
	},
});
