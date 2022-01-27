frappe.ui.form.on('Sales Order Item', {
    quantity: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if(row.qty){
            frappe.model.set_value(cdt, cdn, 'quantity', Math.round(row.qty));
        }
    }
});

