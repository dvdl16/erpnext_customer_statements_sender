// Copyright (c) 2020, Dirk van der Laarse and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Statements Sender', {
  refresh: function (frm) {
    // Default values in From and To Dates
    var today = frappe.datetime.nowdate();
    frm.set_value('from_date', frappe.datetime.month_start(today));
    frm.set_value('to_date', today);
  },
  get_customer_emails: function (frm) {
    frappe.call({
      method: "populate_recipient_list",
      doc: frm.doc,
      callback: function (r) {
        cur_frm.refresh_field('recipients');
        cur_frm.save();
      }
    });
  },
  send_customer_statements: function (frm) {
    let validRecipients = frm.doc.recipients.filter(c => c.send_statement === "Yes").length;
    frappe.confirm(
      'Are you sure you want to send Customer Statement Emails to <b>' + validRecipients + '</b> customers?',
      function () {
        frappe.call({
          method: "erpnext_customer_statements_sender.api.statements_sender_scheduler",
          args: {
            manual: true
          },
          callback: function (r) {
          }
        });
      },
      function () {
        window.close();
      }
    );
  },
  enqueue_sending_statements: function (frm) {
    let validRecipients = frm.doc.recipients.filter(c => c.send_statement === "Yes").length;
    frappe.confirm(
      'Are you sure you want to enqueue Customer Statement Emails to <b>' + validRecipients + '</b> customers?',
      function () {
        frappe.call({
          method: "erpnext_customer_statements_sender.api.statements_sender_scheduler",
          args: {
            manual: false
          },
          callback: function (r) {
          }
        });
      },
      function () {
        window.close();
      }
    );
  },
  preview: function (frm) {
    if (frm.doc.customer != undefined && frm.doc.customer != "") {
      frappe.call({
        method: "erpnext_customer_statements_sender.api.get_report_content",
        args: {
          company: frm.doc.company,
          customer_name: frm.doc.customer,
          from_date: frm.doc.from_date,
          to_date: frm.doc.to_date
        },
        callback: function (r) {
          var x = window.open();
          x.document.open().write(r.message);
        }
      });
    }
    else {
      frappe.msgprint('Please select a customer');
    }
  },
  letter_head: function (frm) {
    cur_frm.save();
  },
  no_ageing: function (frm) {
    cur_frm.save();
  },
  send_email: function (frm) {
    if (frm.doc.customer != undefined && frm.doc.customer != "") {
      frappe.call({
        method: "erpnext_customer_statements_sender.api.send_individual_statement",
        args: {
          company: frm.doc.company,
          customer: frm.doc.customer,
          from_date: frm.doc.from_date,
          to_date: frm.doc.to_date,
          email_id: "to_find"
        },
        callback: function (r) {
          frappe.msgprint(__("Email queued to be sent to customer"))
        }
      });
    }
    else {
      frappe.msgprint('Please select a customer');
    }
  },

});
