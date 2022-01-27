function excess(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if(row.qty && row.excess_percentage!=null){
        frappe.model.set_value(cdt, cdn, 'qty', Math.round(row.qty));
        frappe.model.set_value(cdt, cdn, 'excess', Math.round(row.qty * (row.excess_percentage/100)));
        frappe.model.set_value(cdt, cdn, 'work_order_qty', row.qty + row.excess - row.actual_qty);
    }
  }
  frappe.ui.form.on('Sales Order Item', {
  
  excess_percentage:function(frm, cdt, cdn){
  excess(frm, cdt, cdn);
  },
  qty:function(frm, cdt, cdn){
  excess(frm, cdt, cdn)
  }
  });
  