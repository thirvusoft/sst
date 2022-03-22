import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import make_work_orders

	def on_submit(self):
		self.get_work_order_items()   