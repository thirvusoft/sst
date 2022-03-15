Core - Line Number:51 to 52
  Version - 13.19.0
  Core Path: erpnext/manufacturing/doctype/bom/bom.js
   Existing Code:
    ```
    "item_code": doc.item
    
    ```
   Code to be changed:
    ```
    	"item_code": doc.item,
			"filter_by_item_group": 1
    
    ```
