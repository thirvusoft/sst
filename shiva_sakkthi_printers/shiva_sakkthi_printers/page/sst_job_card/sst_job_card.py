import frappe
@frappe.whitelist()
def workorder(so):
    a= frappe.get_all("Work Order",filters={"sales_order":so})
    return a