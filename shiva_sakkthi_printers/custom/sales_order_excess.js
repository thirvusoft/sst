function excess(frm, cdt, cdn) {
  var row = locals[cdt][cdn];
  if(row.quantity && row.excess_percentage){
      frappe.model.set_value(cdt, cdn, 'quantity', Math.round(row.quantity));
      frappe.model.set_value(cdt, cdn, 'excess', Math.round(row.quantity * (row.excess_percentage/100)));
      frappe.model.set_value(cdt, cdn, 'qty', row.quantity + row.excess);
  }
}
frappe.ui.form.on('Sales Order Item', {

excess_percentage:function(frm, cdt, cdn){
excess(frm, cdt, cdn);
},
quantity:function(frm, cdt, cdn){
excess(frm, cdt, cdn)
}
});
