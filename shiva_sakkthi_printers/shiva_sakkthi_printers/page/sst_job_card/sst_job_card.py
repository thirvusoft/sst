
import frappe

from erpnext.stock.dashboard.item_dashboard import get_data
@frappe.whitelist()
def workorder(so):
    a= frappe.get_all("Work Order",filters={"sales_order":(so)})
    b=frappe.get_value("Sales Order","SAL-ORD-2022-00027","customer")
    x=[]
    for i in a:
        i.customer=b
        x.append(i)
    return x
    
    
    
@frappe.whitelist()
def sofilter(status='',customer=''):
    filters={'status':['!=',"Completed"]}
    if(customer!=""):
      filters['customer']=customer
    so=salesorder=[i.name for i in frappe.get_all("Sales Order",filters)]
    if(status!=''):
      salesorder=[]
      for sales in so:
        tag=frappe.get_value("Sales Order",sales,"_user_tags")
        print(tag,sales)
        if(tag!=None):
          if(status in tag.split(',')):
            salesorder.append(sales)
    return ['']+salesorder
    
    
    
@frappe.whitelist()
def setup():
  filters={'status':['!=',"Completed"]}
  return { 
  "tags":['']+[i.name for i in frappe.get_all("Tag")],
  "salesorder":['']+[i.name for i in frappe.get_all("Sales Order",filters=filters)],
  "customer":list(set(['']+[ i.customer for i in frappe.get_all("Sales Order",filters=filters,fields="customer")]))
  }
  
  
@frappe.whitelist()
def jobcarddetails(salesorder):
  if(salesorder!=''):
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder})]
    work_order_dict=[{'workorder':i.item_name,'qty':i.qty, 'produced_qty':i.produced_qty,
      'in_process':i.material_transferred_for_manufacturing-i.produced_qty,'raw_material':i.required_items[0].item_name,'raw_material_qty':i.required_items[0].required_qty}
      for i in work_order]
    return jobcardhtml(work_order_dict) if(len(work_order_dict)>0) else ''


def jobcardhtml(wo):
  style='''<style> 
              tr,th, td{
                border: 1px solid black;
              } 
              table{
                width:100%;
              }
          </style>'''
  html='<tr>'+''.join([f'<th>{i}</th>' for i in ['S.No','Item Name','Quantity','Stock','Produced Quantity','Production in process','Paper','No of Paper']])+'</tr>'
  td=['<tr>'+f'<td>{wo_details+1}</td>'+''.join([f'<td>{wo[wo_details][list(wo[wo_details].keys())[i]]}</td>' for i in range(len(wo[wo_details]))])+'</tr>' for wo_details in range(len(wo))]
  return style+'<table>'+html+''.join(td)+'</table>'