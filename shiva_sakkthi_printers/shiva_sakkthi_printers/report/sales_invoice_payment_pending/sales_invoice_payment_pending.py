# Copyright (c) 2022, Thirvu Soft Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literals
#from webbrowser import get
from frappe import _
import frappe


# def execute(filters=None):
#     print(filters)
#     columns, data = [] , []
#     columns = get_columns()

#     invoice_details = frappe.get_list('Salses Invoice', {'name', 'posting_date', 'due_date', 'po_no', ''})    print(repack_items)
#     print(frappe.get_list('Stock Entry Detail', {'item_code', 'item_name', 'qty', 'batch_no', 'parent'}))
#     pr_items = frappe.get_list('Purchase Receipt Item', {'item_code', 'item_name', 'qty', 'batch_no', 'parent'})
#     final_data = []
#     for row in pr_items:
#         purchase_item_wise_se_list = frappe.get_list('Stock Entry Detail', {'item_code':row['item_code'], 'batch_no':row['batch_no']},['parent'])
#         total_paruppu_qty = 0
#         for row1 in purchase_item_wise_se_list:
#             total_paruppu_qty += sum(frappe.get_list('Stock Entry Detail', {'item_code':'T4'}, ['qty'],pluck='qty'))
#         final_data.append({'supplier':frappe.db.get_value('Purchase Receipt', row['parent'], 'supplier'),
#                             'item_code':row['item_code'],
#                             'item_name':row['item_name'],
#                             'batch_no':row['batch_no'],
#                             'total_qty':row['qty'],
#                             'total_paruppu_qty': total_paruppu_qty,
#                             'profit_percentage':(total_paruppu_qty/row['qty'])*100 if total_paruppu_qty else 0})
#     return columns, final_data

def execute(filters=None):
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data

def get_data(filters):
	if(filters.party and filters.status):
		party = filters.party
		status = filters.status
		#frappe.errprint(party)
	#	frappe.errprint(status)
	
		
# 	final =[]
# 	final_dict = {}
# 	final_dict['date'] = 1
# 	final_dict['invoice_number'] = 2
# 	final_dict['pdd']  = 3
# 	final_dict['pono'] = 4
# 	final_dict['pod'] = 5
# 	final_dict['tot_amnt'] = 6
# 	final_dict['out_amnt'] = 7
# 	final_dict['status'] = 8
# 	final.append(final_dict)
# 	return final
	data = []
	document_list = frappe.get_list("Sales Invoice",filters={'customer':party,'status':status},fields=['name'],pluck='name')
	frappe.errprint(document_list)
	for doc in document_list:
		document = frappe.get_doc("Sales Invoice",doc)
		final_dict = {}
		final_dict['date'] = document.posting_date
		final_dict['invoice_number'] = doc
		final_dict['pdd']  = document.due_date
		final_dict['pono'] = document.po_no
		final_dict['pod'] = document.po_date
		final_dict['tot_amnt'] = document.rounded_total
		final_dict['out_amnt'] = document.outstanding_amount
		final_dict['status'] = document.status
		data.append(final_dict)
		frappe.errprint(data)
	return data


	# else:
	# 	document_list = frappe.get_list("Sales Invoice",pluck='name')
	# 	frappe.errprint(document_list)
	# 	for doc in document_list:
	# 		document = frappe.get_doc("Sales Invoice",doc)
	# 		final_dict = {}
	# 		final_dict['date'] = document.posting_date
	# 		final_dict['invoice_number'] = doc
	# 		final_dict['pdd']  = document.due_date
	# 		final_dict['pono'] = document.po_no
	# 		final_dict['pod'] = document.po_date
	# 		final_dict['tot_amnt'] = document.rounded_total
	# 		final_dict['out_amnt'] = document.outstanding_amount
	# 		final_dict['status'] = document.status
	# 		final_list.append(final_dict)
	# 		frappe.errprint(final_list)
	#return final_list

def get_columns(filters):
	columns = [
		{
			"label": _("Date"),
			"fieldname":"date",
			"fieldtype":"Data",
			"width":150
		},
		{
			"label": _("Invoice No"),
			"fieldname":"invoice_number",
			"fieldtype":"Link",
			"width":150
		},
		{
			"label": _("Payment Due Date"),
			"fieldname":"pdd",
			"fieldtype":"Data",
			"width":150
		},
		{
			"label": _("PO No"),
			"fieldname":"pono",
			"fieldtype":"Int",
			"width":150
		},
		{
			"label": _("PO Date"),
			"fieldname":"pod",
			"fieldtype":"Data",
			"width":150
		},
		{
			"label": _("Total Amount"),
			"fieldname":"tot_amnt",
			"fieldtype":"Data",
			"width":150
		},
		{
			"label": _("Outstanding Amount"),
			"fieldname":"out_amnt",
			"fieldtype":"Data",
			"width":150
		},
		{
			"label": _("Status"),
			"fieldname":"status",
			"fieldtype":"Data",
			"width":150
		},
	]
	return columns