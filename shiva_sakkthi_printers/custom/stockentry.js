frappe.ui.form.on('Stock Entry Details',{
    after_insert:function(frm,cdt,cdn){
        var row=locals[cdt][cdn];
        frappe.model.set_value(cdt,cdn,row.qty,round(row.qty));
        console.log(row.qty,'\n'*5)
    }
});