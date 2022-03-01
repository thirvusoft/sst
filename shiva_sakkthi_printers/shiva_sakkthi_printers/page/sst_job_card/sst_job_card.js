frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  let page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    

    page.set_indicator('Manufacturing order', 'green')
    let $btn = page.set_primary_action('Start', () =>open_work_order(), true )
    //page.add_menu_item('Send Email', () => open_email_dialog())
    //page.add_inner_button('New Post', () => new_post(), 'Work Order')

   // let $btn = page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync')
    this.form = new frappe.ui.FieldGroup({
    fields: [
      {
        label: 'Tag',
        fieldtype: 'Link',
        fieldname: 'status',
        options:"Tag",
        
    },

    {
      fieldtype: 'Column Break'
    },


  {
    label: 'Sales Order',
    fieldtype: 'Link',
    fieldname: 'salesorder',
    options: 'Sales Order',
    "get_query":function() {
      return {
        filters :{ "_user_tags":",HIGH"}
          
      }
    },

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
      fieldname:"preview"
    }

  ],
    body: this.page.body
   } );
   
   this.form.make();
   
   
  function open_work_order() {
    frappe.set_route("work-order");
    }  
/*
  
  frappe.call({
      method: "shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.workorder",
      args:{
        so: "SAL-ORD-2022-00027"
      },
      callback: function(r) {
        console.log(r.message)
        for(let i=0;i<r.message.length;i++){
        page.add_field({
          label: 'Customer Name',
          fieldtype: 'Data',
          fieldname: 'customer_name',
       
        })
        page.add_field({
          label: 'Work Order',
          fieldtype: 'Read Only',
          fieldname: 'workorder',
          default: r.message[i].name
       
        })
        
      } }
    });
    for(let i=0;i<3;i++){
    this.form.get_field('preview').html(`
   aaa
		`);
    }*/
}


