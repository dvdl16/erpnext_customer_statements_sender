# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_customer_statements_sender"
app_title = "ERPNext Customer Statements Sender"
app_publisher = "Dirk van der Laarse"
app_description = "This app allows you to send out statements to your customers in bulk"
app_icon = "fa fa-envelope"
app_color = "blue"
app_email = "dirk@laarse.co.za"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_customer_statements_sender/css/erpnext_customer_statements_sender.css"
# app_include_js = "/assets/erpnext_customer_statements_sender/js/erpnext_customer_statements_sender.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_customer_statements_sender/css/erpnext_customer_statements_sender.css"
# web_include_js = "/assets/erpnext_customer_statements_sender/js/erpnext_customer_statements_sender.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_customer_statements_sender.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Custom Jinja Filters
# ----------
jenv = {
	"methods": [
		"format_value:erpnext_customer_statements_sender.api.frappe_format_value"
	]
}

# Installation
# ------------

# before_install = "erpnext_customer_statements_sender.install.before_install"
# after_install = "erpnext_customer_statements_sender.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_customer_statements_sender.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_customer_statements_sender.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_customer_statements_sender.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_customer_statements_sender.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_customer_statements_sender.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_customer_statements_sender.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_customer_statements_sender.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_customer_statements_sender.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_customer_statements_sender.task.get_dashboard_data"
# }

fixtures = [
    {"dt":"Custom Field", "filters": [["dt", "in", ("Customer", "Contact")], ["fieldname", "in", ("disable_customer_statements", "is_customer_statement_contact")]]}
]
