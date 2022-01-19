frappe.ui.form.on('Sales Order Item', {
  quantity: function (frm, cdt, cdn) {
      var row = locals[cdt][cdn];
      if(row.quantity){
          frappe.model.set_value(cdt, cdn, 'quantity', math.round(row.quantity));
          frappe.model.set_value(cdt, cdn, 'excess', math.round(row.quantity * (5/100)));
          frappe.model.set_value(cdt, cdn, 'qty', row.quantity + row.excess);
      }
  }
});

