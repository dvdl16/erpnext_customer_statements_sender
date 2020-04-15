// Copyright (c) 2020, Dirk van der Laarse and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Statements Sender', {
  refresh: function(frm) {
    // Hide Add Row button
    $('div[id="page-Form/Customer Statements Sender"] div.small.form-clickable-section.grid-footer').css({'display': 'none'});
  },
	get_customer_emails: function(frm) {
    frappe.call({
      method: "populate_recipient_list",
      doc: frm.doc,
      callback: function(r) {
          cur_frm.refresh_field('recipients');
      }
    });
	}
});
