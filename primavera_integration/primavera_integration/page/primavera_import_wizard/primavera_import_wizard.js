// Copyright (c) 2026, Raissyon Trading & Contracting Co.
//
// "Primavera Import" wizard page.
//
// Phase 1 scope: upload an XER file, pick the target ERPNext Project
// (existing or new), and create the Primavera Import record. Parsing and
// preview are triggered from here but their actual implementation lives
// in the Sync Engine phase — see tasks/parse_import.py.

frappe.pages["primavera-import-wizard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Primavera Import",
		single_column: true,
	});

	new PrimaveraImportWizard(page);
};

class PrimaveraImportWizard {
	constructor(page) {
		this.page = page;
		this.state = {
			file_url: null,
			project_mode: "Existing Project",
			target_erpnext_project: null,
			new_project_name: null,
			import_name: null,
		};
		this.render_upload_step();
	}

	reset_body() {
		this.page.body.empty();
	}

	step_header(title, step_no) {
		return $(`<div class="pv-step-header">
			<span class="indicator-pill blue">${__("Step")} ${step_no}</span>
			<h4 style="display:inline-block;margin-left:8px;">${title}</h4>
		</div>`);
	}

	// ---- Step 1: Upload ----
	render_upload_step() {
		this.reset_body();
		this.page.body.append(this.step_header(__("Upload XER File"), 1));

		const $wrapper = $('<div class="pv-upload-wrapper" style="margin-top:15px;"></div>').appendTo(
			this.page.body
		);

		new frappe.ui.FileUploader({
			restrictions: {
				allowed_file_types: [".xer"],
				max_number_of_files: 1,
			},
			on_success: (file_doc) => {
				this.state.file_url = file_doc.file_url;
				$wrapper.append(
					`<div class="text-success" style="margin-top:10px;">
						${__("Uploaded")}: ${frappe.utils.escape_html(file_doc.file_name)}
					</div>`
				);
				this.render_continue_button($wrapper, () => this.render_project_step());
			},
		});
	}

	render_continue_button($container, on_click) {
		$(`<button class="btn btn-primary btn-sm" style="margin-top:15px;">${__("Continue")}</button>`)
			.appendTo($container)
			.on("click", on_click);
	}

	// ---- Step 2: Project selection ----
	render_project_step() {
		this.reset_body();
		this.page.body.append(this.step_header(__("Select ERPNext Project"), 2));

		const $form = $(`
			<div style="margin-top:15px; max-width:480px;">
				<div class="form-group">
					<label>${__("Mode")}</label>
					<select class="form-control" id="pv-project-mode">
						<option value="Existing Project">${__("Use an existing ERPNext Project")}</option>
						<option value="Create New Project">${__("Create a new ERPNext Project")}</option>
					</select>
				</div>
				<div class="form-group" id="pv-existing-project-wrap">
					<label>${__("ERPNext Project")}</label>
					<input class="form-control" id="pv-existing-project" placeholder="${__("Start typing a project name")}">
				</div>
				<div class="form-group" id="pv-new-project-wrap" style="display:none;">
					<label>${__("New Project Name")}</label>
					<input class="form-control" id="pv-new-project-name">
				</div>
			</div>
		`).appendTo(this.page.body);

		// Existing-project autocomplete via a lightweight link field.
		this.project_control = frappe.ui.form.make_control({
			parent: $form.find("#pv-existing-project-wrap"),
			df: {
				fieldtype: "Link",
				options: "Project",
				fieldname: "target_erpnext_project",
				label: "",
				onchange: () => {
					this.state.target_erpnext_project = this.project_control.get_value();
				},
			},
			render_input: true,
		});
		this.project_control.refresh();

		$form.find("#pv-project-mode").on("change", (e) => {
			const mode = $(e.target).val();
			this.state.project_mode = mode;
			$form.find("#pv-existing-project-wrap").toggle(mode === "Existing Project");
			$form.find("#pv-new-project-wrap").toggle(mode === "Create New Project");
		});

		$form.find("#pv-new-project-name").on("change", (e) => {
			this.state.new_project_name = $(e.target).val();
		});

		this.render_continue_button($form, () => this.create_import_and_parse());
	}

	// ---- Step 3: Create the Primavera Import record and enqueue parsing ----
	create_import_and_parse() {
		if (
			this.state.project_mode === "Existing Project" &&
			!this.state.target_erpnext_project
		) {
			frappe.msgprint(__("Select an existing ERPNext Project, or switch to Create New Project."));
			return;
		}
		if (this.state.project_mode === "Create New Project" && !this.state.new_project_name) {
			frappe.msgprint(__("Enter a name for the new ERPNext Project."));
			return;
		}

		frappe.call({
			method: "frappe.client.insert",
			args: {
				doc: {
					doctype: "Primavera Import",
					xer_file: this.state.file_url,
					project_mode: this.state.project_mode,
					target_erpnext_project: this.state.target_erpnext_project,
					new_project_name: this.state.new_project_name,
				},
			},
			freeze: true,
			freeze_message: __("Creating import record..."),
			callback: (r) => {
				this.state.import_name = r.message.name;
				frappe.call({
					method: "frappe.client.get_doc",
					args: { doctype: "Primavera Import", name: this.state.import_name },
					callback: (doc_r) => {
						frappe.call({
							doc: doc_r.message,
							method: "queue_parse",
							callback: () => this.render_progress_step(),
						});
					},
				});
			},
		});
	}

	// ---- Step 4: Progress / result ----
	render_progress_step() {
		this.reset_body();
		this.page.body.append(this.step_header(__("Parsing"), 3));

		const $status = $(`<div style="margin-top:15px;"></div>`).appendTo(this.page.body);
		$status.append(
			`<p>${__("Parsing has been queued as a background job.")}</p>` +
				`<a class="btn btn-default btn-sm" href="/app/primavera-import/${this.state.import_name}">
					${__("Open Import Record")}
				</a>`
		);

		frappe.msgprint({
			title: __("Queued"),
			message: __(
				"Note: the XER parser itself ships in the next phase — this record will stay " +
					"in an honest 'Uploaded' state with an explanatory note until then. " +
					"The upload, project selection, and background-job wiring are fully " +
					"functional now."
			),
			indicator: "blue",
		});
	}
}
