Core - Line Number:330 & 331
  Version - 13.19.0
  Core Path: erpnext/controllers/item_variant.py
   Existing Code:
    ```
    variant.item_code = "{0}-{1}".format(template_item_code, "-".join(abbreviations))
		variant.item_name = "{0}-{1}".format(template_item_name, "-".join(abbreviations))

    
    ```
   Code to be changed:
    ```
    	variant.item_code = "{0}/{1}".format(template_item_code, "/".join(abbreviations))
	  	variant.item_name = "{0}/{1}".format(template_item_name, "/".join(abbreviations))
    
    ```
