function excess(frm) {
  if(frm.quantity && frm.excess_percentage!=Null){
      frappe.model.set_value(frm, 'quantity', Math.round(frm.quantity));
      frappe.model.set_value(frm, 'excess', Math.round(frm.quantity * (frm.excess_percentage/100)));
      frappe.model.set_value(frm, 'qty', frm.quantity + frm.excess);
  }
}
frappe.ui.form.on('Work Order', {

excess_percentage:function(frm){
excess(frm);
},
quantity:function(frm){
excess(frm)
}
});
