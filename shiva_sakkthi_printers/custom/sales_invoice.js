frappe.ui.form.on('Sales Invoice',{
refresh:function(frm){
    var taxes_and_charges= cur_frm.doc.taxes_and_charges;
    cur_frm.set_value('taxes_and_charges','');
    cur_frm.set_value('taxes_and_charges',taxes_and_charges)
}
})
