Core - Line Number:84 to 101
  Version - 13.19.0
  Core Path: erpnext/public/js/controllers/buying.js
   Existing Code:
    ```
    if (me.frm.doc.is_subcontracted == "Yes") {
				return{
					query: "erpnext.controllers.queries.item_query",
					filters:{ 'supplier': me.frm.doc.supplier, 'is_sub_contracted_item': 1 }
				}
			}
			else {
				return{
					query: "erpnext.controllers.queries.item_query",
					filters: { 'supplier': me.frm.doc.supplier, 'is_purchase_item': 1 }
				}
			}
		});
    
    ```
   Code to be changed:
    ```
    		// 	if (me.frm.doc.is_subcontracted == "Yes") {
				return{
		// 			query: "erpnext.controllers.queries.item_query",
		//	filters:{ 'supplier': me.frm.doc.supplier, 'is_sub_contracted_item': 1 }
		     filters: {
		       	'item_group' : 'By-Product'
		     }
				}
		 });   
		// 		}
		// 	}
		// 	else {
		// 		return{
		// 			query: "erpnext.controllers.queries.item_query",
		// 			filters: { 'supplier': me.frm.doc.supplier, 'is_purchase_item': 1 }
		// 		}
		// 	}
		// });
    
    ```
