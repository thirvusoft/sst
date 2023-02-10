frappe.ui.form.on('Sales Invoice',{
    refresh:function(frm){
        if(!cur_frm.doc.taxes){
            var taxes_and_charges= cur_frm.doc.taxes_and_charges;
            cur_frm.set_value('taxes_and_charges','');
            cur_frm.set_value('taxes_and_charges',taxes_and_charges)
        }
        frm.add_custom_button(__('Generate E-Way Bill'), function () {
            frappe.call({
                // "method":"shiva_sakkthi_printers.custom.sales_invoice.generate_ewb",
                "method":"erpnext.regional.india.utils.generate_ewb",
                "args":{
                    "doc":frm.doc
                }
            })
        }, __('Actions'));
    },
   
})