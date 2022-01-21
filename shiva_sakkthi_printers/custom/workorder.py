from erpnext.stock.utils import get_latest_stock_qty
def updateqty(self,event):
   self.qty-=get_latest_stock_qty(self.item_name,self.fg_warehouse)
    