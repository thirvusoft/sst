Core - Line Number:5+
  Version - 13.19.0
  Core Path: erpnext/manufacturing/doctype/work_order/work_order.py
   Existing Code:
    ``` 
    ```
   Code to be changed:
    ```
     import math
    
    ```
    
Core - Line Number:283,284
   Existing Code:
    ``` 
    	d.required_qty = item_dict.get(d.item_code).get("qty")
    
    ```
   Code to be changed:
    ```
      print('\n'*5,d.available_qty_at_wip_warehouse,item_dict.get(d.item_code).get("qty"))
			d.required_qty = math.ceil(item_dict.get(d.item_code).get("qty"))
    
    ```
