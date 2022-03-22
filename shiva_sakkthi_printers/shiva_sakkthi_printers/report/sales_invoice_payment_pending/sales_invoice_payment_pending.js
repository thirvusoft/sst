// Copyright (c) 2022, Thirvu Soft Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Invoice Payment Pending"] = {
	"filters": [
		{
			"fieldname":"doctype",
			"label": __("Type"),
			"fieldtype":"Read Only",
			"default":"Sales Invoice",
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype":"Read Only",
			"default":"Customer",
		},
		{
			"fieldname":"party",
			"label":__("Party"),
			"fieldtype":"Link",
			"options":"Customer",
		},
		{
			"fieldname":"status",
			"label":__("Status"),
			"fieldtype":"Select",
			"default":"",
			"options":["","Partly Paid","Payment Pending"],
		},

	]
};
