Core - Line Number:78
  Version - 13.19.0
  Core Path: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
   Existing Code:
    ```
    self.indicator_title = _("Unpaid")
    
    ```
   Code to be changed:
    ```
    	self.indicator_title = _("Payment Pending")
    
    ```
    
    
Core - Line Number:1514
  
  Existing Code:
    ```
    	self.status = "Unpaid"
    
    ```
   Code to be changed:
    ```
    	self.status = "Payment Pending"
    
    ```
    
    
    Core - Line Number:1526
  
  Existing Code:
    ```
    	self.status in ("Unpaid", "Partly Paid", "Overdue")
    
    ```
   Code to be changed:
    ```
    	self.status in ("Payment Pending", "Partly Paid", "Overdue")
    
    ```
