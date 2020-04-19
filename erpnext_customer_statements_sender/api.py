from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, today, cint, add_days, get_link_to_form, format_time, global_date_format, now, get_url_to_report
from frappe.utils.xlsxutils import make_xlsx
from frappe.utils.pdf import get_pdf
from frappe import _
import json
from pprint import pprint
from frappe.www import printview

@frappe.whitelist()
def send_statements(company=None):

	if company is None:
		company = frappe.db.get_single_value('Customer Statements Sender', 'company')
		if not company:
			frappe.throw(_('Company field is required on Customer Statements Sender'))
			exit()

	email_list = get_recipient_list()
	for row in email_list:
		if row.email_id is not None:
			if row.send_statement == "Yes":
				data = get_report_content(company, row.customer)
				if not data:
					return

				attachments = [{
					'fname': get_file_name(),
					'fcontent': data
				}]

				# frappe.sendmail(
				# 	recipients = row.email_id,
				# 	subject = f'Customer Statement from {company}',
				# 	message = f'Good day. <br> Please find attached your latest statement from {company}',
				# 	attachments = attachments,
				# 	reference_doctype = "Report",
				# 	reference_name="General Ledger"
				# )

	frappe.msgprint('Emails queued for sending')

def get_report_content(company, customer_name):
	'''Returns file in for the report in given format'''

	# Borrowed code from frappe/email/doctype/auto_email_report/auto_email_report.py
	report = frappe.get_doc('Report', "General Ledger")

	custom_filter = {
					'company': company,
					'party_type': 'Customer',
					'party': [customer_name],
					'from_date': add_days(today(), -90),
					'to_date': today(),
					'group_by': 'Group by Voucher (Consolidated)'}

	columns, data = report.get_data(limit=500, user = "Administrator", filters = custom_filter, as_dict=True)

	# add serial numbers
	columns.insert(0, frappe._dict(fieldname='idx', label='', width='30px'))
	for i in range(len(data)):
		data[i]['idx'] = i+1

	# Get Letter Head
	no_letterhead = bool(frappe.db.get_single_value('Customer Statements Sender', 'no_letter_head'))
	doc = frappe.get_doc('Customer Statements Sender', 'Customer Statements Sender')
	letter_head = frappe._dict(printview.get_letter_head(doc, no_letterhead) or {})

	if letter_head.content:
		letter_head.content = frappe.utils.jinja.render_template(letter_head.content, {"doc": doc.as_dict()})

	print(get_billing_address(customer_name))

	date_time = global_date_format(now()) + ' ' + format_time(now())
	report_html_data = frappe.render_template('erpnext_customer_statements_sender/templates/report/customer_statement_jinja.html', {
		'title': f'Customer Statement for {customer_name}',
		'description': f'Customer Statement for {customer_name}',
		'date_time': date_time,
		'columns': columns,
		'data': data,
		'report_name': f'Customer Statement for {customer_name}',
		'filters': custom_filter,
		'letter_head': letter_head.content,
		'billing_address': get_billing_address(customer_name)
	})

	print(report_html_data)

	pdf_data = get_pdf(report_html_data)
	return pdf_data


def get_file_name():
	return "{0}.{1}".format("Customer Statement".replace(" ", "-").replace("/", "-"), "pdf")


def get_billing_address(customer):
	addresses = frappe.db.sql("""SELECT
								customer,
								MAX(priority) AS preferred_address,
								address_line1,
								address_line2,
								city,
								county,
								state,
								country,
								postal_code
							FROM
								(SELECT
										tab_cus.name AS 'customer',
										tab_add.name AS 'address_title',
										IFNULL(tab_add.is_primary_address, 0) AS 'priority',
										tab_add.address_line1,
										tab_add.address_line2,
										city,
										county,
										state,
										country,
										pincode AS 'postal_code'
									FROM `tabCustomer` AS tab_cus
										INNER JOIN `tabDynamic Link` as tab_dyn ON tab_dyn.link_name = tab_cus.name AND tab_dyn.link_doctype = 'Customer'
										INNER JOIN `tabAddress` as tab_add ON tab_dyn.parent = tab_add.name AND tab_dyn.parenttype = 'Address'
									WHERE tab_cus.name = 'Spar' AND tab_add.address_type = 'Billing') AS t_billing_add
							GROUP BY customer""", as_dict=True)
	if addresses and len(addresses)>0:
		del(addresses[0]['preferred_address'])
		return addresses[0]
	else:
		return {}




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
									LEFT JOIN `tabDynamic Link` as tab_dyn ON tab_dyn.link_name = tab_cus.name AND tab_dyn.link_doctype = 'Customer' AND tab_dyn.parenttype = 'Contact'
									LEFT JOIN `tabContact` as tab_con ON tab_dyn.parent = tab_con.name
								WHERE tab_cus.disabled = 0) AS t_contacts
							GROUP BY customer
							ORDER BY customer""", as_dict=True)
