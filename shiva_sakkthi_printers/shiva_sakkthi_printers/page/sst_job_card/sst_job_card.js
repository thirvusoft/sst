frappe.pages['sst-job-card'].on_page_load = function(wrapper) {
  let page = frappe.ui.make_app_page({
        title: 'JOB CARD',
        parent: wrapper,
        single_column: true
    });
    

    page.set_indicator('Manufacturing order', 'green')
    let $btn = page.set_primary_action('Start',()=>open_work_order())
    

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
    function open_work_order() {
        frappe.set_route("work-order");
    }

     
}


