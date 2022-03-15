Core - Line Number:300+  to 322+
  Version - 13.19.0
  Core Path: erpnext/selling/doctype/sales_order/sales_order.js
   Existing Code:
    ```
    	}, {
							fieldtype: 'Float',
							fieldname: 'pending_qty',
							reqd: 1,
							label: __('Qty'),
							in_list_view: 1
						}, {

    
    ```
   Code to be changed:
    ```
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
    
    ```
