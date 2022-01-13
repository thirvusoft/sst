import frappe
def autoname(self,event):
    item_name=self.customer_name[:2]+'-'+self.brand[:2]+'-'+self.sub_style
    try:
        attrTab=self.attributes
        item_name+='-'+('-'.join([frappe.db.get_value('Item Attribute Value',
			{'attribute_value': i.attribute_value}, 'abbr') for i in attrTab]))

    except:
        pass
    
    self.item_code=item_name.upper()
    self.name=self.item_code