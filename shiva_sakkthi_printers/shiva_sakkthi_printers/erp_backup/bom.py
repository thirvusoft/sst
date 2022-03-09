Core - Line Number:1133+, 1134+
  Version - 13.19.0
  Core Path: erpnext/manufacturing/doctype/bom/bom.py
   Existing Code:
    ```
   
    
    ```
   Code to be changed:
    ```
    	if filters and filters.get('filter_by_item_group'):
		  query_filters['item_group'] = 'By-Product'
    
    ```
