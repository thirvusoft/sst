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
    report_data = frappe.db.sql(""" select si.posting_date,si.customer,si.po_no,si.name,
                                        si.rounded_total,si.outstanding_amount,si.due_date,si.status
                                    from `tabSales Invoice` as si 
                                    left outer join `tabCustomer` as cus on
                                        cus.customer_name = si.customer
                                    left outer join `tabAddress` as ad on
                                        ad.parent = cus.name
                                    {0}
                                """.format(conditions))
    
    report_data=list(report_data)
    a=frappe.get_all('Address')
    for i in range(len(report_data)):
        fadd=None
        add=[]
        for x in list(a):
            doc=frappe.get_doc('Address',x.name)
            for j in doc.links:
                if(j.link_name==report_data[i][1]):
                    add.append(doc)
        for x in add:
            if(x.is_primary_address==1):
                fadd=x.email_id
        report_data[i]+=(fadd,)

    columns, data = get_columns(), report_data
    return columns, data
def get_columns():
    columns = [
        _("Date") + ":date:100",
        _("Customer Name") + ":Link/Customer:130",
        _("PO NO") + ":data:100",
        _("Invoice No") + ":Link/Sales Invoice:130",
        _("Total Amount") + ":Currency:150",
        _("Outstading Amount") + ":Currency:150",
        _("Due Date") + ":date:100", 
        _("Status") + ":data:100",

        _("Email id") + ":Link/Address:150" 

          ]
    return columns