import frappe
from erpnext.stock.dashboard.item_dashboard import get_data

def makese(type,wo,item,bom,qty,sw='Finished Goods - SST',ww='Work in Progress - SST',fw='Dispatch - SST'):
    doc=frappe.new_doc('Stock Entry')
    doc.update(dict(
    stock_entry_type=type,
    work_order=wo,
    from_bom=1,
    bom_no=bom,
    fg_completed_qty=qty,
    ))
    items=[dict(
        s_warehouse=sw,
        t_warehouse=ww,
        item_code=item,
        qty=qty,
        uom='Nos',
    )]
    if(type=='Manufacture'):
            items=[dict(
            s_warehouse=ww,
            item_code=item,
            qty=qty,
            uom='Nos',
        ),dict(
            t_warehouse=fw,
            item_code=item,
            qty=qty,
            uom='Nos',
        )        ]
    doc.set('items',items)
    doc.save()
    doc.submit()
    
def workorder(self,action):
    qty=get_data(item_code=self.production_item , warehouse="Finished Goods - SST")
    if(qty!=[]):
        qty=qty[0]['actual_qty']
        if(qty>self.qty):
            qty=self.qty
        for type in ['Material Transfer For Manufacture','Manufacture']:
            makese(type,self.name,self.production_item,self.bom_no,qty,fw=self.fg_warehouse)
        if(self.move_excess_stock):
            frappe.db.set(self, "excess_stock", qty)
        else:
            frappe.db.set(self, "excess_stock", 0)