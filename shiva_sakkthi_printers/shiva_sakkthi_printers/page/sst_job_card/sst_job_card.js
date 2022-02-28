frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  let page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    

    page.set_indicator('Manufacturing order', 'green')
    let $btn = page.set_primary_action('Start', () =>open_work_order(frm), true )
    //page.add_menu_item('Send Email', () => open_email_dialog())
    //page.add_inner_button('New Post', () => new_post(), 'Work Order')

   // let $btn = page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync')
   let field = page.add_field({
        label: 'Tag',
        fieldtype: 'Select',
        fieldname: 'status',
        options: [
            'High',
            'Low',
            'Medium'
        ],
        change() {
            console.log(field.get_value());
        }
    });
      //  field = page.add_field({
      //  label: 'Customer',
      //  fieldtype: 'Link',
      //  fieldname: 'customer',
      //  options: 'Sales Order',
      //  change() {
       //     console.log(field.get_value());
      //  }
   // });
  function open_work_order(frm) {
        frappe.new_doc('Work Order', {
           work_order: frm.doc.name
            })
    }
     
}



 // page.start = 0;

 // page.warehouse_field = page.add_field({
   //       fieldname: 'warehouse',
     //     label: __('Warehouse'),
       //   fieldtype:'Link',
         // options:'Warehouse',
          //change: function() {
            //      page.item_dashboard.start = 0;
              //    page.item_dashboard.refresh();
        //  }
  //});

  //page.customer_field= page.add_filed({
    //      fieldname:"customer",
      //    label:__('Customer'),
        //  fieldtype:'Link',
          //options:'Customer',
         // change: function() {
           //       page.sales_order_dashboard.start = 0;
             //     page._dashboard.refresh();
          //}

  //});
//}

