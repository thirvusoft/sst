Core - Line Number:1133+, 1134+
  Version - 13.19.0
  Core Path: erpnext/accounts/doctype/sales_invoice/sales_invoice_list.js
   Existing Code:
    ```
   
    
    ```
   Code to be changed:
    ```
    	if filters and filters.get('filter_by_item_group'):
		  query_filters['item_group'] = 'By-Product'
    
    ```
