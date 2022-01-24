import frappe
from erpnext.stock.utils import get_latest_stock_qty
def updateqty(self,event):
   self.qty-=get_latest_stock_qty(self.item_name,self.fg_warehouse)
   items=self.get('required_items')
   print(items)
   for item in items:
      print(item.required_qty)
      item.required_qty-=item.available_qty_at_wip_warehouse
      print(item)
      print(item.required_qty)
      print('\n'*3)
   self.save()
   self.reload()
      