Core - Line Number:91 to 103
  Version - 13.19.0
  Core Path: erpnext/buying/doctype/purchase_order/purchase_order.js
   Existing Code:
    ```
    frappe.ui.form.on("Purchase Order Item", {
	schedule_date: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.schedule_date) {
			if(!frm.doc.schedule_date) {
				erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "schedule_date");
			} else {
				set_schedule_date(frm);
			}
		}
	}
});
    
    ```
   Code to be changed:
    ```
    	comment (/*  */)
    
    ```
