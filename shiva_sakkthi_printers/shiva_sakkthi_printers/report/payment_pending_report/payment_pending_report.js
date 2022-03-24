// Copyright (c) 2022, Thirvu Soft Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Payment Pending Report"] = {
	"filters": [
		 {

		
              "fieldname":"name",
		 				 "label": __("Invoice Type"),
		 				 "fieldtype":"Select",
		 				 "options": ["Sales Invoice"],
		 				 "default": "Sales Invoice"
		 },
		 {
										
							"fieldname":"party_type",
		 					"label": __("Party Type"),
		 					"fieldtype":"Select",
		 					"options": ["Customer"],
		 					"default": "Customer"
		 },
		{
										
		        	"fieldname":"customer",
	        		"label": __("Customer"),
	        		"fieldtype":"Link",
		        	"options": "Customer"
   },
	 {
										
							"fieldname":"status",
							"label": __("Status"),
							"fieldtype":"Select",
							"options": ["","Partly Paid", "Payment Pending"]
  },
	],
	onload: function(report) {
		report.page.add_inner_button(__("Send Email"), function() {
			 var myWin = window.open('https://mail.google.com/mail/u/0/#inbox?compose=new');
		}).addClass("btn-warning").css({'color':'blue','font-weight': 'bold'});

	}
	
};
