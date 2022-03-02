frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  let page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    
    page.set_indicator('Manufacturing order', 'green')
    page.set_primary_action('Start', () =>open_work_order(), true )
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
     // "get_query":function() {
      //  return {
       //   filters :{ "_user_tags":",HIGH"}
          
       // }
      //}
      onchange:function(){
        if(this.value){
          console.log(this)
          frappe.call({
            method: "shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_job_card.sst_job_card.workorder",
            args:{
              salesorder: this.value
            },
            callback:function(r){
              console.log(r["message"])
              this.customer_name.set_value(r["message"]);
              this.customer_name.refresh()
          
              console.log("setted")
            }
        })

        }

      }
     },
     // function filter() {
     //   var keyword = document.getElementById("search").value;
     //   var select = document.getElementById("select");
       // for (var i = 0; i < select.length; i++) {
       //     var txt = select.options[i].text;
       //     if (!txt.match(keyword)) {
            //    $(select.options[i]).attr('disabled', 'disabled').hide();
        //    } else {
        //        $(select.options[i]).removeAttr('disabled').show();
         //   }

       // }
    
     
     {
      fieldtype: 'Section Break'
     },
     {
      label: 'Customer Name',
      fieldtype: 'Data',
      fieldname: 'customer_name',
    },


      /*{
      fetch_from: "salesorder.customer",
      label: 'Customer Name',
      fieldtype: 'Read Only',
      fieldname: 'customer_name',
      },
      {
      fieldtype: 'Section Break'
      },*/
     {
      fieldtype:"HTML",
      fieldname:"preview",
    
     }
    

     ],
     body: this.page.body
     } );
    
     this.form.make();
    
   
   //make_form()
  function open_work_order() {
    frappe.set_route("work-order");
    }  

  
  
      /*
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
    for(let i=0;i<3;i++){*/
    this.form.get_field('preview').html(`
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }
    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    table, th, td {
      border:1px solid black;
      border-collapse: collapse;
    }
      
    </style>
    <div id="orange" style="position:relative">
    <table>
      <tr>
        <th><center>S.No</center></th>
        <th><center>Design Name/Size</center></th>
        <th><center>Qantity</center></th>
        <th><center>Stock</center></th>
        <th><center>Production</center></th>
        <th><center>No Of Paper</center></th>
      </tr>

      
        <c:forEach>
      <tr>
        <td><center>{{<%= i %> <% i++; %>}}</center></td>
        <td>{{}}</td>
        <td>{{}}}</td>
        <td>{{}}}</td>
        <td>{{}}}</td>
        <td>{{}}}</td>
      </tr>
      </c:if>
    </table>
    </div>
    
		`);
    
}


