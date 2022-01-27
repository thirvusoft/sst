frappe.ui.form.on("Sales Order Item", {
	setup: function(frm) {
		frm.set_query("item_code", function() {
		    let customer=frm.doc.customer;
			return {
				filters: [
					['customer_name','=',customer]
				]
			}
		});
	}
});
© 2022 GitHub, Inc.
