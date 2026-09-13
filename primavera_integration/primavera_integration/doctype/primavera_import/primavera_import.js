// Copyright (c) 2026, Raissyon Trading & Contracting Co.

frappe.ui.form.on("Primavera Import", {
	refresh: function (frm) {
		if (frm.doc.status === "Uploaded" && frm.doc.xer_file && !frm.is_new()) {
			frm.add_custom_button(__("Parse XER"), function () {
				frm.call("queue_parse").then(() => frm.reload_doc());
			}).addClass("btn-primary");
		}

		if (frm.doc.status === "Parsing") {
			frm.dashboard.set_headline(
				__("Parsing is running in the background. Refresh to check progress.")
			);
		}

		if (frm.doc.preview_status === "Ready") {
			frm.add_custom_button(__("View Preview"), function () {
				frappe.msgprint(
					__("The Preview screen ships with the Sync Engine phase; this button is wired to it once that phase lands.")
				);
			});
		}
	},

	project_mode: function (frm) {
		frm.toggle_reqd("target_erpnext_project", frm.doc.project_mode === "Existing Project");
		frm.toggle_reqd("new_project_name", frm.doc.project_mode === "Create New Project");
	},
});
