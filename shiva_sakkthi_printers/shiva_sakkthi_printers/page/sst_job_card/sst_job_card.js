frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  var page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    
    new erpnext.JOBCARD(page);
  }


  erpnext.JOBCARD=class JOBCARD {
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
          method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.sofilter",
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
        method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.sofilter",
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
          method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.jobcarddetails",
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
      "options":'<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head>'
    }
    
  ],
  body: this.page.body
  })
  this.form.make();
  frappe.call({
    method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.setup",
  callback:function(r){
    this.form.get_input("tag").empty().add_options(r.message.tags);
    this.form.get_input("salesorder").empty().add_options(r.message.salesorder);
    this.form.get_input("customer").empty().add_options(r.message.customer);
  }.bind(this)
  })
}
}