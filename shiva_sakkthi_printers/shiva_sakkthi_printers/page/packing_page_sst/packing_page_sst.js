frappe.pages['packing-page-sst'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'PACKING',
		single_column: true
	});
	new erpnext.PACKING(page);
}

erpnext.PACKING=class PACKING {
    constructor(page) {
      this.page = page;
      this.make_form();
    }
    make_form(){
  this.form = new frappe.ui.FieldGroup({
  fields: [
    {
      "label":"Customer",
      "fieldname":"customer",
      "fieldtype":"Select",
      "change" : () => frappe.call(
        {
          method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.packing_page_sst.packing_page_sst.sofilter",
          args:{
            "customer":this.form.get_value("customer"),
            "status":this.form.get_value("tag")
          },
          callback:function(r){
            this.form.get_input("salesorder").empty().add_options(r.message);
          }.bind(this)
        })
    },
    {
      "fieldtype":"Column Break"
    },
    {
      "label":"Tag",
      "fieldname":"tag",
      "fieldtype":"Select",
      "change" : () => frappe.call(
      {
        method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.packing_page_sst.packing_page_sst.sofilter",
        args:{
          "status":this.form.get_value("tag"),
          "customer":this.form.get_value("customer"),
        },
        callback:function(r){
          this.form.get_input("salesorder").empty().add_options(r.message);
        }.bind(this)
      })
    },
    {
      "fieldtype":"Column Break"
    },
    {
      "label":"Sales Order",
      "fieldname":"salesorder",
      "fieldtype":"Select",
      "change" : () => frappe.call(
        {
          method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.packing_page_sst.packing_page_sst.jobcarddetails",
          args:{
            "salesorder":this.form.get_value("salesorder")
          },
          callback: function(r){
            this.form.get_field('jobcard').html(r.message)
          }.bind(this)
        }
      )
    },
    {
      "fieldtype":"Section Break"
    },
    {
      "fieldtype":"HTML",
      "fieldname":"jobcard",
    }
    
  ],
  body: this.page.body
  })
  this.form.make();
  frappe.call({
    method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.packing_page_sst.packing_page_sst.setup",
  callback:function(r){
    this.form.get_input("tag").empty().add_options(r.message.tags);
    this.form.get_input("salesorder").empty().add_options(r.message.salesorder);
    this.form.get_input("customer").empty().add_options(r.message.customer);
  }.bind(this)
  })
}
}