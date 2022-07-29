frappe.ui.form.on('BOM', {
    refresh: function(frm){
        frm.set_query('item_code', 'items', function(frm){
            return {
                filters: {
                    'item_group': 'Raw Material'
                }
            }
        })
    }
})