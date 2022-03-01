import frappe
@frappe.whitelist()
def workorder(so):
    a= frappe.get_all("Work Order",filters={"sales_order":so})
    b=frappe.get_value("Sales Order","SAL-ORD-2022-00027","customer")
    x=[]
    for i in a:
        i.customer=b
        x.append(i)
    return x
@frappe.whitelist()
def sofilter(status):
    if(status==""):
        salesorder=[i.name for i in frappe.get_all("Sales Order")]
    else:
        so=frappe.get_all("Sales Order")
        salesorder=[]
        for i in so:
            if(frappe.get_value("Sales Order",i.name,"_user_tags")!=None):
                if(status in frappe.get_value("Sales Order",i.name,"_user_tags")):
                   salesorder.append(i.name)
    ret="\\n".join(salesorder)
    return ret