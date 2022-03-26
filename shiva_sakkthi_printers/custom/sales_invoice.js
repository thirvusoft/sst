frappe.ui.form.on('Sales Invoice',{
refresh:function(frm){
    var a= cur_frm.doc.taxes_and_charges;
    cur_frm.set_value('taxes_and_charges','');
    cur_frm.set_value('taxes_and_charges',a)
}
})