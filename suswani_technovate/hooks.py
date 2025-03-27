app_name = "suswani_technovate"
app_title = "Suswani Technovate"
app_publisher = "Bhavy Jhaveri"
app_description = "Suswani"
app_email = "bhavy.jhaveri@technovate.in"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "suswani_technovate",
# 		"logo": "/assets/suswani_technovate/logo.png",
# 		"title": "Suswani Technovate",
# 		"route": "/suswani_technovate",
# 		"has_permission": "suswani_technovate.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/suswani_technovate/css/suswani_technovate.css"
# app_include_js = "/assets/suswani_technovate/js/suswani_technovate.js"

# include js, css files in header of web template
# web_include_css = "/assets/suswani_technovate/css/suswani_technovate.css"
# web_include_js = "/assets/suswani_technovate/js/suswani_technovate.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "suswani_technovate/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "suswani_technovate/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "suswani_technovate.utils.jinja_methods",
# 	"filters": "suswani_technovate.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "suswani_technovate.install.before_install"
# after_install = "suswani_technovate.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "suswani_technovate.uninstall.before_uninstall"
# after_uninstall = "suswani_technovate.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "suswani_technovate.utils.before_app_install"
# after_app_install = "suswani_technovate.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "suswani_technovate.utils.before_app_uninstall"
# after_app_uninstall = "suswani_technovate.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "suswani_technovate.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"suswani_technovate.tasks.all"
# 	],
# 	"daily": [
# 		"suswani_technovate.tasks.daily"
# 	],
# 	"hourly": [
# 		"suswani_technovate.tasks.hourly"
# 	],
# 	"weekly": [
# 		"suswani_technovate.tasks.weekly"
# 	],
# 	"monthly": [
# 		"suswani_technovate.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "suswani_technovate.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "suswani_technovate.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "suswani_technovate.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["suswani_technovate.utils.before_request"]
# after_request = ["suswani_technovate.utils.after_request"]

# Job Events
# ----------
# before_job = ["suswani_technovate.utils.before_job"]
# after_job = ["suswani_technovate.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"suswani_technovate.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

