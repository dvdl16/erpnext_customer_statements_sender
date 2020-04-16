# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dirk van der Laarse and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext_customer_statements_sender.api import get_recipient_list

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
