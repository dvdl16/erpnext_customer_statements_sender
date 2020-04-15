# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dirk van der Laarse and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomerStatementsSender(Document):
	def populate_recipient_list(self):
	# Get list of customers and email addresses, append to table
		self.recipients = [];
		customer_list = get_recipient_list()
		for c in customer_list:
			row = self.append('recipients', {})
			row.customer = c.customer
			row.contact = c.contact
			row.email = c.email_id
			row.send_statement = c.send_statement

@frappe.whitelist()
def get_recipient_list():
	return frappe.db.sql("""SELECT
								customer,
								contact,
								email_id,
								MIN(priority) AS priority,
								send_statement
							FROM
								(SELECT
									tab_cus.name AS 'customer',
									tab_con.name AS 'contact',
									tab_con.email_id,
									CASE WHEN is_customer_statement_contact = 1 THEN 1 WHEN tab_con.is_primary_contact = 1 THEN 2 ELSE 3 END AS 'priority',
									CASE WHEN tab_cus.disable_customer_statements = 1 THEN 'No (Disabled for this customer)' WHEN ISNULL(tab_con.email_id) OR tab_con.email_id = '' THEN 'No (No email address on record)' ELSE 'Yes' END AS 'send_statement'
								FROM `tabCustomer` AS tab_cus
									LEFT JOIN `tabDynamic Link` as tab_dyn ON tab_dyn.link_name = tab_cus.name AND tab_dyn.link_doctype = 'Customer'
									LEFT JOIN `tabContact` as tab_con ON tab_dyn.parent = tab_con.name AND tab_dyn.parenttype = 'Contact'
								WHERE tab_cus.disabled = 0) AS t_contacts
							GROUP BY customer
							ORDER BY customer""", as_dict=True)
