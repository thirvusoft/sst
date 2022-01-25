frappe.ui.form.on('Sales Order Item', {
    quantity: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if(row.quantity){
            console.log('cs')
            frappe.model.set_value(cdt, cdn, 'quantity', Math.round(row.quantity));
            frappe.model.set_value(cdt, cdn, 'excess', Math.round(row.quantity * (5/100)));
            frappe.model.set_value(cdt, cdn, 'qty', row.quantity + row.excess);
        }
    }
});

