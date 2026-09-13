# Primavera Integration (for ERPNext v15)

Phase 1 scope: XER file import, staging DocTypes, Project/Activity/Resource
mapping, preview-before-sync data model, and the UI foundation (Workspace +
Primavera Import wizard page).

**Not yet implemented in this phase** (by design — see architecture doc):
the XER parser itself, the sync engine that writes to ERPNext Project/Task,
the API/XML adapters, and two-way sync. Those land in the next phase on top
of this data model.

## Install

```bash
# from your bench directory
bench get-app primavera_integration /path/to/primavera_integration
bench --site your-site install-app primavera_integration
bench --site your-site migrate
```

## Tests

```bash
bench --site your-site run-tests --app primavera_integration
```
