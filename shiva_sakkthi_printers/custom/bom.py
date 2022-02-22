import frappe
def create_bom_for_variants(self):
    if(self.has_variants==1):
        item_template=self.item
    else:
        item_template=frappe.get_value("Item",self.item,"variant_of")
    #variants without BOM
    items=frappe.get_all("Item",filters={"variant_of":item_template})
    item_bom=[i.name for i in items if(frappe.get_all("BOM",filters={"item":i.name})==[])]
    items=item_bom
    #creating BOM
    for variant in item_bom:
        bom=frappe.new_doc("BOM")
        bom.update(dict(
            doctype="BOM",
            item=variant,
            quantity=self.quantity,
            price_list_currency=self.price_list_currency,
            raw_material_cost=self.raw_material_cost,
            base_raw_material_cost=self.base_raw_material_cost,
            total_cost=self.total_cost,
            base_total_cost=self.base_total_cost,
        ))
        bom_list=[]
        for i in self.items:
            bom_list.append({
                "item_code" : i.item_code,
                "qty" : i.qty,
                "uom" : i.uom,
                "rate" : i.rate
            })
        bom.set('items', bom_list)
        bom.save()
        bom.submit()
        



def createbom(self,event):
    if(self.bom_variant==1):
        create_bom_for_variants(self)