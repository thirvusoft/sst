# Copyright (c) 2022, Thirvu Soft Private Limited and contributors
# For license information, please see license.txt

# from multiprocessing import Condition
# from xml.dom.minidom import Document
import frappe
from frappe import _
def execute(filters=None):
    customer = filters.get("customer")
    status = filters.get("status")
    conditions = "where 1 = 1 "
    if customer:
        conditions += " and si.customer = '{0}' ".format(customer)
    if status:
        conditions += " and si.status ='{0}' ".format(status)
    report_data = frappe.db.sql(""" select si.posting_date,si.customer,si.name,
                                        si.total,si.outstanding_amount,si.due_date
                                    from `tabSales Invoice` as si
                                    {0}
                                """.format(conditions))
    columns, data = get_columns(), report_data
    return columns, data
def get_columns():
    columns = [
        _("Date") + ":date:100",
        _("Customer Name") + ":Link/Customer:130",
        _("Invoice No") + ":Link/Sales Invoice:130",
        _("Total Amount") + ":Currency:100",
        _("Outstading Amount") + "Currency:100",
        _("Due Date") + ":date:100"    ]
    return columns