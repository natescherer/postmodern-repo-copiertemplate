// Scoped to this one page rather than a site-wide pymdownx.tasklist clickable_checkbox
// config change, which would make every task list on the docs site clickable -- most
// docs don't have one, and the ones that do shouldn't opt in silently. This only
// removes the disabled attribute pymdownx.tasklist renders by default (the same DOM
// change clickable_checkbox itself makes), so checkboxes are toggleable purely as a
// visual scratchpad -- see the doc's own warning about state not being saved.
if (location.pathname.includes("manual_verification")) {
  document.querySelectorAll(".task-list-item input[type=checkbox]").forEach((checkbox) => {
    checkbox.disabled = false;
  });
}
