# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document
# from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, today, cint, add_days, get_link_to_form
# from frappe import _
# from frappe.utils.xlsxutils import make_xlsx
# import json
#
#
# @frappe.whitelist()
# def send_statements():
#
# 	email_list = frappe.db.get_values('Send Customer Statements Customers', {'parent': 'Send Customer Statements'}, ['customer_name','email','send_statement'])
# 	for customer_name, email, send_statement in email_list:
# 		if email is not None:
# 			if send_statement == "Yes":
# 				data = get_report_content(customer_name)
# 				if not data:
# 					return
#
# 				attachments = [{
# 					'fname': get_file_name(),
# 					'fcontent': data
# 				}]
#
# 				frappe.sendmail(
# 					recipients = email,
# 					subject = "Customer Statement from Simply Garlic",
# 					message = "Good day. <br> Please find attached your latest statement from Simply Garlic",
# 					attachments = attachments,
# 					reference_doctype = "Report",
# 					reference_name="General Ledger"
# 				)
#
# 	frappe.msgprint('Emails queued for sending')
#
# def get_report_content(customer_name):
# 	'''Returns file in for the report in given format'''
#
# 	# Borrowed code from frappe/email/doctype/auto_email_report/auto_email_report.py
# 	report = frappe.get_doc('Report', "General Ledger")
# 	custom_filter = {'company': "Horizon Global SA (Pty) Ltd", 'party_type': "Customer", 'party': customer_name, 'from_date': add_days(today(), -7),'to_date': today(), 'group_by': "Group by Voucher (Consolidated)"}
#
# 	columns, data = report.get_data(limit=100 or 100, user = "Administrator", filters = custom_filter, as_dict=True)
#
# 	# add serial numbers
# 	columns.insert(0, frappe._dict(fieldname='idx', label='', width='30px'))
# 	for i in range(len(data)):
# 		data[i]['idx'] = i+1
#
# 	# For .xlsx
# 	spreadsheet_data = get_spreadsheet_data(columns, data)
# 	xlsx_file = make_xlsx(spreadsheet_data, "Auto Email Report")
# 	return xlsx_file.getvalue()
#
# 	# For .html
# 	# columns, data = make_links(columns, data)
# 	# return self.get_html_table(columns, data)  <-------------Fails here....... see auto_email_report.py
#
#
# def get_spreadsheet_data(columns, data):
# 	out = [[_(df.label) for df in columns], ]
# 	for row in data:
# 		new_row = []
# 		out.append(new_row)
# 		for df in columns:
# 			if df.fieldname not in row: continue
# 			new_row.append(frappe.format(row[df.fieldname], df, row))
#
# 	return out
#
# def get_file_name():
# 	return "{0}.{1}".format("Customer Statement".replace(" ", "-").replace("/", "-"), "xlsx")
# 	# return "{0}.{1}".format("Customer Statement".replace(" ", "-").replace("/", "-"), "html")
#
#
# # def make_links(columns, data):
# # 	for row in data:
# # 		for col in columns:
# # 			if col.fieldtype == "Link" and col.options != "Currency":
# # 				if col.options and row.get(col.fieldname):
# # 					row[col.fieldname] = get_link_to_form(col.options, row[col.fieldname])
# # 			elif col.fieldtype == "Dynamic Link":
# # 				if col.options and row.get(col.fieldname) and row.get(col.options):
# # 					row[col.fieldname] = get_link_to_form(row[col.options], row[col.fieldname])
# #
# # 	return columns, data
