frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  let page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    
var a="\nSAL-ORD-2022-00027\nSAL-ORD-2022-00016";
    page.set_indicator('Manufacturing order', 'green')
    page.set_primary_action('Start', () =>open_work_order(), true )
    x = new frappe.ui.FieldGroup({
    fields: [
      {
        label: 'Tag',
        fieldtype: 'Link',
        fieldname: 'status',
        options:"Tag",
        change : () => frappe.call({
            method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.sofilter",
            args:{
              "status":x.get_value("status")
            },
            callback:function(r){
              a=r.message;
              console.log(a);
              x.get_field('salesorder').set_value(a);  
            }
          })
      },

      {
      fieldtype: 'Column Break'
      },
      {
      label: 'Sales Order',
      fieldtype: "Select",
      fieldname: 'salesorder',
      options:a,
      change: () => frappe.call({
        method: "shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.workorder",
        args:{
          so: x.get_value("salesorder")
        },
        callback: function(r) {
          console.log(r.message)
          page.clear_fields();
          for(let i=0;i<r.message.length;i++){
          page.add_field({
            label: 'Customer Name',
            fieldtype: 'Read Only',
            fieldname: 'customer_name',
            default: r.message[i].customer
         
          })
          page.add_field({
            label: 'Work Order',
            fieldtype: 'Read Only',
            fieldname: 'workorder',
            default: r.message[i].name
         
          })
        page.add_field({
          fieldtype:"HTML",
          options:"<hr>"
        })
        } }
      })
      },
      {
      fieldtype: 'Section Break'
      },
      {
      fetch_from: "salesorder.customer",
      label: 'Customer Name',
      fieldtype: 'Read Only',
      fieldname: 'customer_name',
      },
      {
      fieldtype: 'Section Break'
      },
      {
      fieldtype:"HTML",
      fieldname:"preview",
      options:"bbb"
      }

     ],
      body: this.page.body
    } );
   
   x.make();
   
   
  function open_work_order() {
    frappe.set_route("work-order");
    }  
}


