from . import __version__ as app_version

app_name = "shiva_sakkthi_printers"
app_title = "Shiva Sakkthi Printers"
app_publisher = "Thirvu Soft Private Limited"
app_description = "Handling entire flow of Shiva Sakkthi Printers"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "core@thirvusoft.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shiva_sakkthi_printers/css/shiva_sakkthi_printers.css"
# app_include_js = "/assets/shiva_sakkthi_printers/js/shiva_sakkthi_printers.js"

# include js, css files in header of web template
# web_include_css = "/assets/shiva_sakkthi_printers/css/shiva_sakkthi_printers.css"
# web_include_js = "/assets/shiva_sakkthi_printers/js/shiva_sakkthi_printers.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shiva_sakkthi_printers/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Item" : "/custom/item.js" ,
	"Stock Entry" : "/custom/stockentry.js",
	"Sales Order" : "/custom/sales_order.js",
	"BOM"         : "/custom/bom.js",
	"Sales Invoice":"/custom/sales_invoice.js",
	"Item Variant Settings" : "/custom/item_variant_settings.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {"Sales Order" : "/custom/sales_order_list.js"}

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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "shiva_sakkthi_printers.install.before_install"
# after_install = "shiva_sakkthi_printers.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shiva_sakkthi_printers.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"BOM" : {
		"on_submit":"shiva_sakkthi_printers.custom.bom.createbom"
	},
	"Work Order":{
		"on_submit":"shiva_sakkthi_printers.custom.stockentry.workorder",
		"validate":"shiva_sakkthi_printers.custom.work_order.change_warehouse"
	},
	"Sales Order":{
		 "after_insert":"shiva_sakkthi_printers.custom.sales_order.abcd"
	}
 }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"shiva_sakkthi_printers.tasks.all"
# 	],
# 	"daily": [
# 		"shiva_sakkthi_printers.tasks.daily"
# 	],
# 	"hourly": [
# 		"shiva_sakkthi_printers.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shiva_sakkthi_printers.tasks.weekly"
# 	]
# 	"monthly": [
# 		"shiva_sakkthi_printers.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "shiva_sakkthi_printers.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shiva_sakkthi_printers.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "shiva_sakkthi_printers.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"shiva_sakkthi_printers.auth.validate"
# ]

