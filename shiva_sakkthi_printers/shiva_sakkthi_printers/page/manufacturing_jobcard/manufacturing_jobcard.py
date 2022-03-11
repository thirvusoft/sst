from re import S
import frappe
from erpnext.stock.dashboard.item_dashboard import get_data
    
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
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":['!=','Cancelled'],"docstatus":1})]
    work_order_dict=[{
      'workorder':i.item_name,
      'qty':int(i.qty),
      'stock':0 if(get_data(item_code=frappe.get_all("Item",{"item_name":i.item_name})[0].name , warehouse="Finished Goods - SST")==[]) else int(get_data(item_code=frappe.get_all("Item",{"item_name":i.item_name})[0].name , warehouse="Finished Goods - SST")[0]['actual_qty']) ,
      'raw_material_qty':int(i.required_items[0].required_qty)  }  for i in work_order]
    seperated_work_order=workorderfunc(work_order_dict)
    status=[ i.status for i in work_order]
    workorder=[i.name for i in work_order]
    htmlcode=jobcardinfohtml(salesorder)
    for workorderdict in seperated_work_order:
        htmlcode+=jobcardhtml(workorderdict,seperated_work_order[workorderdict],status,salesorder,workorder)
    htmlcode+=description(work_order_dict)
    return htmlcode if(len(work_order_dict)>0) else '<center><b> NO JOB CARDS </b></center>'
 
 
 
def workorderfunc(wo):
    seperated_work_order={}
    for i in wo:
        itemcode=frappe.get_all('Item',{'item_name':i['workorder']})
        item=frappe.get_doc('Item',itemcode[0].name)
        for attr in item.attributes:
            if(attr.attribute=='Colour'):
                color=attr.attribute_value
        if(color in seperated_work_order):
            seperated_work_order[color].append(i)
        else:
            seperated_work_order[color]=[i]
    return seperated_work_order
        
        
        
        
 
def statusindicator(status):
  color={
    "In Process": "orange",
    "Completed": "green",
    "Not Started": "red",
    "Stopped": "red",
    "Closed": "black",
    "Cancelled": "red"
  }
  return f'<span class="indicator-pill whitespace-nowrap {color[status]}"><span style="font-weight:bold;font-size:14px;">{status}</span></span>'


  
def script():
  scr= f'''
    <script>
      function start(wo){{
        console.log('hiii',wo);
        frappe.set_route("work-order",wo);
        location.reload();
      }}
    </script>
  '''
  return scr


def button(wo):
  return f'''
    <button onclick="start('{wo}')" class="start" type="button" style="background-color:#4da6ff; margin-bottom:4px;"> Start </button>
  '''



def progress(produced,inprocess,not_started):
  bar=f'''
    <div class="progress">
      <div class="progress-bar bg-success" style="width:{produced}%">
        <b>Produced {produced}</b>
      </div>
      <div class="progress-bar bg-warning" style="width:{inprocess}%;font-color:white">
        <b>Inprocess {inprocess}</b>
      </div>
      <div class="progress-bar bg-gray" style="width:{not_started}%">
        <b>Not Started {not_started}</b>
      </div>
    </div> 
  '''
  return bar



def jobcardinfohtml(salesorder):
  so=frappe.get_doc('Sales Order',salesorder)
  infohtml=f'''
    <div class='div'>
      <div class='jobcardinfo'>
        Customer Name : {so.customer}<br>
        Delivery Date : {so.delivery_date}<br><br>
      </div>
      <div class='jobcardinfo'>
        Job Card NO : {so.name}<br>
        PO No : {so.po_no}<br><br>
      </div>
    </div>
  '''
  return infohtml


def description(wo):
  print('\n'*5,wo)
  total_papers=sum([i['raw_material_qty'] for i in wo])
  print(total_papers,'\n'*3)
  return f'''
    <div class='div'>
    Total No of Papers: {total_papers}
    </div>
  '''


def html_style():
  style='''
    <style>
      td{
        padding: 6px;
      }
      .table1{
        width: 100%;
        margin-bottom: 5px;
      }
      .heading{
        font-weight: bold;
        border: 1px solid black;
        width: 10%;
      }
      .data{
        border: 1px solid black;
      }
    </style>
  '''
  return style


def no_of_paper(wo):
  return f'''
      <b>
        No of Papers: {sum([i["raw_material_qty"] for i in wo])}
      </b>'''



def jobcardhtml(color,wo,status,salesorder,workorder):
  wo_list=list(zip(*[list(i.values()) for i in wo]))
  html_code=[]
  colorhtml=f'''
    <b> Colour: {color}</b>
  '''
  trs=['<tr><td class="heading">Size</td>',
       '<tr><td class="heading">Qty</td>',
       '<tr><td class="heading">Stock</td>',
       '<tr><td class="heading">No of Paper</td>']  
  table='<table class="table1">'
  for i,j in zip(trs,wo_list):
    table+=i+''.join( [f'<td class="data">{x}</td>' for x in j] )+'</tr>'
  html_code.append(html_style())
  html_code.append(colorhtml)
  html_code.append(table+'</table>'+no_of_paper(wo)+'<BR><br><br>')
  return ''.join(html_code)
    
    
