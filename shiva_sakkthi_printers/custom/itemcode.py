def autoname(self,event):
    item_name=self.customer_name[:2]+'-'+self.brand[:2]+'-'+self.sub_style[:2]
    try:
        attrTab=self.attributes
        item_name+='-'+('-'.join([i.attribute_value[:2] for i in attrTab]))
    except:
        pass
    self.item_code=item_name.upper()
    self.name=self.item_code
    
