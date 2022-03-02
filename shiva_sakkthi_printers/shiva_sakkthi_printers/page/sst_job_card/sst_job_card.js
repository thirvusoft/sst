frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  var page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
       
var a="\nSAL-ORD-2022-00027\nSAL-ORD-2022-00016";
    page.set_indicator('Manufacturing order', 'green')
    page.set_primary_action('Start', () =>open_work_order(), true )
   page.tag=page.add_field({
        label: 'Tag',
        fieldtype: 'Link',
        fieldname: 'status',
        options:"Tag",
        change : () => frappe.call({
            method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.sofilter",
            args:{
              "status":page["tag"].get_value()
            },
            callback:function(r){
              a=r.message;
              console.log('a',a);
              page['salesorder'].set_value(a); 
              page.salesorder.refresh();
              /*page['preview'].html(`
                <style>
                table, tr{
                  border: 1px solid black;
                  width: 100%;  
                }
                th{
                  text-align:right;
                  border: 1px solid black;
                }
                </style>

                <table>
                  <tr>
                    <th>S.No</th>
                    <th>Design</th>
                    <th>Quantity</th>
                    <th>Stock</th>
                    <th>Production</th>
                    <th>No of Paper</th>
                  </tr>
                </table>

              `);*/
            
            }
          })
      });

      /*{
      fieldtype: 'Column Break'
      },*/
      page.salesorder = page.add_field({
      label: 'Sales Order',
      fieldtype: "Select",
      fieldname: 'salesorder',
      options:a,
      change: () => frappe.call({
        method: "shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.workorder",
        args:{
          so: page['salesorder'].get_value()
        },
        callback: function(r) {
          console.log(r.message)
          
          for(let i=0;i<r.message.length;i++){
            page['tab1'].get_value(`
            <style>
            table, tr{
              border: 1px solid black;
              width: 100%;  
            }
            th{
              text-align:right;
              border: 1px solid black;
            }
            </style>

            <table>
              <tr>
                <th>S.No</th>
                <th>Design</th>
                <th>Quantity</th>
                <th>Stock</th>
                <th>Production</th>
                <th>No</th>
              </tr>
            </table>

          `);
        } }
      })
      });
      
      page.customer = page.add_field({
      fetch_from: "salesorder.customer",
      label: 'Customer Name',
      fieldtype: 'Read Only',
      fieldname: 'customer_name',
      });
      
      page.preview = page.add_field({
      fieldtype:"HTML",
      fieldname:"preview",
      options:'aaa'
      });
      page.tab1 = page.add_field({
      fieldtype:"HTML",
      fieldname:"tab",
      options:'bbb'
      });

     
   
   
   
  function open_work_order() {
    frappe.set_route("work-order");
    }  

    




}



