frappe.ui.form.on('Stock Entry Detail',{
"after_insert":function(frm,cdt,cdn){
        var row=locals[cdt][cdn];
        frappe.model.set_value(cdt,cdn,'qty',Math.ceil(row.qty));
       console.log('stock entry a',row.qty);
    
}
});