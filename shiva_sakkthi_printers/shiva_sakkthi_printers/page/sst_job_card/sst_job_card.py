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
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":['!=','Cancelled']})]
    work_order_dict=[{'workorder':i.item_name,'qty':int(i.qty),'stock':0 ,'produced_qty':int(i.produced_qty), 
      'in_process':int(i.material_transferred_for_manufacturing-i.produced_qty),'not_started':int(i.qty-i.material_transferred_for_manufacturing),'raw_material':i.required_items[0].item_name,'raw_material_qty':int(i.required_items[0].required_qty)}
      for i in work_order]
    return jobcardhtml(work_order_dict) if(len(work_order_dict)>0) else '<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head>'


def progress(produced,inprocess,not_started):
  bar=f'''
    <div class="progress">
      <div class="progress-bar bg-success" style="width:{produced}%">
        <b>Produced{produced}</b>
      </div>
      <div class="progress-bar bg-warning" style="width:{inprocess}%">
        <b>Inprocess{inprocess}</b>
      </div>
      <div class="progress-bar bg-gray" style="width:{not_started}%">
        <b>Not Started{not_started}</b>
      </div>
    </div> 
  '''
  return bar

def jobcardhtml(wo):
  head='<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head>'
  style='''<style> 
              tr,th, td{
                border-bottom: 1px solid black;
                border-left:1px solid grey;
                height:50px;
                font-size:15px;
                text-align:center;
              } 
              table{
                width:100%;
                border:1px solid black;
              }
          </style>'''
  html='<tr>'+''.join([f'<th>{i}</th>' for i in ['S.No','Item Name','Quantity','Stock','Produced Quantity','Production in process','Production Not Started','Paper','No of Paper']])+'</tr>'
  td=['<tr>'+f'<td>{wo_details+1}</td>'+''.join([f'<td>{wo[wo_details][list(wo[wo_details].keys())[i]]}</td>' for i in range(len(wo[wo_details]))])+f'</tr><tr><td colspan=9>{progress(wo[wo_details]["produced_qty"],wo[wo_details]["in_process"],wo[wo_details]["not_started"])}</td></tr>' for wo_details in range(len(wo))]
  return head+style+'<table>'+html+''.join(td)+'</table>'