
frappe.ui.form.on('Sales Order', {
	customer: function(frm) {
	frm.set_query("style", function() {
		return {
			filters: {
				'customer_name': frm.doc.customer,
				'has_variants':1
			}
		}
	});
},
style: function(frm) {
	frm.set_query("item_code", 'items',function() {
		return {
			filters: {
				'variant_of': frm.doc.style
			}
		};
	});
}
});


// cur_frm.fields_dict('BOM')  
//   frm.get_query(function(doc, cdt, cdn) {
// 	let row=locals[cdt][cdn];	
// 	return {
// 	filters: {
// 		'item_name': frm.doc.item_code
		
// 	}
// 	}
// 	}

function bm(frm,cdt,cdn){
		let row=locals[cdt][cdn];
		frappe.db.get_value("BOM", {"item": row.item_code, 'is_default':1}, ["name","quantity"], (r) => {
			frappe.model.set_value(cdt, cdn, "bom_quantity", r.name);
			frappe.model.set_value(cdt, cdn, "label_count_per_paper", r.quantity);
		});	
	// frm.set_query("bom_quantity",function(frm,cdt,cdn){
	// 	row=locals[cdt][cdn];
	// 	return{
	// 		filters:{'item_name':row.item_code}

	// 	};
	// });
	}

function paper(frm,cdt,cdn){
	let row=locals[cdt][cdn];
	if(row.qty>=0 && row.label_count_per_paper>=0){
	frappe.model.set_value(cdt,cdn,'no_of_sheets',Math.round(row.qty/row.label_count_per_paper));
}
}
frappe.ui.form.on('Sales Order Item', {
qty:function(frm,cdt,cdn){
 paper(frm,cdt,cdn);
},
label_count_per_paper:function(frm,cdt,cdn){
 paper(frm,cdt,cdn);
},
item_code:function(frm, cdt, cdn){
	bm(frm, cdt, cdn)
}
})

//function item(frm,cdt,cdn){
//	 	cur_frm.fields_dict('BOM')  
 // frm.get_query(function(doc, cdt, cdn) {
	//let row=locals[cdt][cdn];	
	//return {
	//filters: {
	//	'item_name': frm.doc.item_code
		
//	}
//}
//});
//}


//frappe.ui.form.on('Sales Order Item', {
//item_code:function(frm,cdt,cdn){
	//frm.set_query("bom_quantity",function(frm,cdt,cdn){
		//row=locals[cdt][cdn];
		//return{
			//filters:{
				//'item_name':row.item_code
			//}
     //item(frm,cdt,cdn);
		//}
	//});
//}
//});