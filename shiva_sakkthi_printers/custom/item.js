frappe.ui.form.on('Item', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0){
			frm.add_custom_button(__('View Design'), function(){
				var myWin = window.open(frm.doc.drive_link);
			});
		}
	},
	has_variants: function(frm){
		if(frm.doc.has_variants==1){
			var new_row = frm.add_child("attributes");
            new_row.attribute="Colour";
            var new_row = frm.add_child("attributes");
            new_row.attribute="Paper Quality";
            var new_row = frm.add_child("attributes");
            new_row.attribute="Size";
		}
		else{
			frm.clear_table("attributes");
		}
		refresh_field("attributes");
	}

});
frappe.ui.form.on('Item', {
	item_group: function(frm) {
		if(cur_frm.doc.item_group=='Products')
			cur_frm.set_value('gst_hsn_code', "49089000");
		else
			cur_frm.set_value('gst_hsn_code', "");
		
}
});

frappe.ui.form.on('Item', {
	item_group:function(frm){
	    if(frm.doc.item_group=="Products"){
	        cur_frm.fields_dict.item_name.set_label('Design Name');
	    }
	    else{
	        cur_frm.fields_dict.item_name.set_label('Item Name'); 
	    }
	}
});
