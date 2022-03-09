Core - Line Number:11+ 
  Version - 13
  Core Path:
   Existing Code:
    ```
    ```
   Code to be changed:
    ```
    from erpnext.stock.dashboard.item_dashboard import get_data
    
    ```
    
Core - Line Number:(410+, 411+ )
  Existing Code:
    ```
    ```
   Code to be changed:
    ```
    	       excess_percentage=0,
							stock= 0 if(get_data(item_code=i.item_code , warehouse='Finished Goods - SST')==[]) else get_data(item_code=i.item_code , warehouse='Finished Goods - SST')[0]['actual_qty'],
    
    ```
    
 Core - Line Number:(423+, 424+ )
   Existing Code:
    ```
    ```
   Code to be changed:
    ```
    	        excess_percentage=0,
							stock= 0 if(get_data(item_code=i.item_code , warehouse='Finished Goods - SST')==[]) else get_data(item_code=i.item_code , warehouse='Finished Goods - SST')[0]['actual_qty'],
    
    ```
    
    Core - Line Number:1025+
       Existing Code:
    ```
       qty=i['pending_qty'],
    
    ```
      Code to be changed:
    ```
    	qty=(((i['pending_qty']-i['stock'])*i['excess_percentage'])/100)+i['pending_qty'],
    	        
    ```
    
  
