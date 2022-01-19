frappe.ui.form.on("Item", {
	setup: function(frm) {
		frm.set_query("brand", function() {
		    let customer_name=frm.doc.customer_name;
			return {
				filters: [
					['customer','=',customer_name]
				]
			}
		});
	}
});