
frappe.ui.form.on('Sales Order', {
	setup:function(frm){
		frm.set_value('items',[])
			frm.set_query("item_template",function(){
					return {
						filters: {
							"has_variants": 1
								}
					};
			})
	},
	item_template:function(frm){
		frappe.call({
			"method":"shiva_sakkthi_printers.custom.sales_order.get_template",
			'args':{
				'item':frm.doc.item_template
			},
			callback:function(res){		
				frm.set_value('attribute_table',[])
				for (let i in res.message){
					var child = frm.add_child('attribute_table')
					frappe.model.set_value('Item Attribute Table',child.name,'attribute',res.message[i])
				}

			}
		})
		frm.refresh();
	},
	get_item:function(frm){
		frappe.call({
			"method":"shiva_sakkthi_printers.custom.sales_order.get_variant",
			'args':{
				'template':frm.doc.item_template,
				'attribute_table':frm.doc.attribute_table
			},
			callback:function(res){	
				console.log(res.message)
				if(res.message && frm.doc.quantity){
					var item = frm.add_child('items')
					frappe.model.set_value(item.doctype,item.name,'item_code',res.message)
					frappe.model.set_value(item.doctype,item.name,'qty',frm.doc.quantity)
				}
				else if(!frm.doc.quantity && res.message){
					frappe.msgprint(`Kindly Enter the quantity for the item ${res.message}`)
				}
				else if(!res.message){
					frappe.msgprint("Item-Variant not found for these attributes")
				}
			}
		})
	},
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
		}
	});
},
// after_save: function(frm) {
// 	console.log('hvyuguihuihiuniunoi')},

after_save: function(frm){
	var me = this;
	this.frm.call({
		doc: this.frm.doc,   
		method: 'get_work_order_items',
		callback: function(r) {
			if(!r.message) {
				frappe.msgprint({
					title: __('Work Order not created'),
					message: __('No Items with Bill of Materials to Manufacture'),
					indicator: 'orange'
				});
				return;
			}
			else if(!r.message) {
				frappe.msgprint({
					title: __('Work Order not created'),
					message: __('Work Order already created for all items with BOM'),
					indicator: 'orange'
				});
				return;
			} else {
				const fields = [{
					label: 'Items',
					fieldtype: 'Table',
					fieldname: 'items',
					description: __('Select BOM and Qty for Production'),
					fields: [{
						fieldtype: 'Read Only',
						fieldname: 'item_code',
						label: __('Item Code'),
						in_list_view: 1
					}, {
						fieldtype: 'Link',
						fieldname: 'bom',
						options: 'BOM',
						reqd: 1,
						label: __('Select BOM'),
						in_list_view: 1,
						get_query: function (doc) {
							return { filters: { item: doc.item_code } };
						}
					},
					{
						fieldtype: 'Int',
						fieldname: 'pending_qty',
						reqd: 1,
						label: __('Qty'),
						in_list_view: 1
					},
					{
						fieldtype: 'Int',
						fieldname: 'excess_percentage',
						reqd: 1,
						label: __('Excess Percentage'),
						in_list_view: 1
					},
					{
						fieldtype: 'Int',
						fieldname: 'stock',
						reqd: 1,
						label: __('Stock'),
						in_list_view: 1
					},
					{
						fieldtype: 'Data',
						fieldname: 'sales_order_item',
						reqd: 1,
						label: __('Sales Order Item'),
						hidden: 1
					}],
					data: r.message,
					get_data: () => {
						return r.message
					}
				}]
				var d = new frappe.ui.Dialog({
					title: __('Select Items to Manufacture'),
					fields: fields,          
				});
				var data = {items: d.fields_dict.items.grid.get_data()};
				me.frm.call({
					method: 'make_work_orders',
					args: {
						items: data,
						company: me.frm.doc.company,
						sales_order: me.frm.docname,
						project: me.frm.project
					},
					freeze: true,
					callback: function(r) {
						if(r.message) {
							alert(r.message)
							// frappe.msgprint({
							//   message: __('Work Orders Created: {0}', [r.message.map(function(d) {
							//       return repl('<a href="/app/work-order/%(name)s">%(name)s</a>', {name:d})
							//     }).join(', ')]),
							//   indicator: 'green'
							// })
						}
					}
				});      }
		}
	});
}.bind(this)
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


frappe.ui.form.on('Item Attribute Table', {
	attribute:function(frm,cdt,cdn){
			let row = locals[cdt][cdn]
				frappe.call({
					"method":"shiva_sakkthi_printers.custom.sales_order.get_attribute_value",
					'args':{
						'attribute':row.attribute
					},
					callback:function(res){		
						var df = frappe.meta.get_docfield('Item Attribute Table',"value",row.name);
						df.options = res.message

					}
				})
				frm.refresh();
		}
});
