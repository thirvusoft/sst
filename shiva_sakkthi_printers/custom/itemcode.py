import frappe
def autoname(self,event):
    if(None in [self.customer_name,self.brand,self.sub_style] and self.item_group!='By-Product'):
        frappe.throw('Mandatory Fields: Customer name, Brand, Sub style')
        if(len(self.customer_name)<2 and len(self.brand)<2):
            frappe.throw('Customer name and Brand must contain more than two letters')
    if(self.item_name==None):
        frappe.throw('Mandatory Fields: Item name')

    if(self.item_group=='By-Product'):
        self.item_code=self.item_name
        self.name=self.item_name
        return

    item_name=self.customer_name[:2]+'-'+self.brand[:2]+'-'+self.sub_style
    try:
        attrTab=self.attributes
        item_name+='-'+('-'.join([frappe.db.get_value('Item Attribute Value',
			{'attribute_value': i.attribute_value}, 'abbr') for i in attrTab]))

    except:
        pass
    
    self.item_code=item_name.upper()
    self.name=self.item_code
    
   