frappe.ui.form.on('Item', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0){
		frm.add_custom_button(__('View Design'), function(){
			var myWin = window.open(frm.doc.drive_link);
	});
}
}
});

