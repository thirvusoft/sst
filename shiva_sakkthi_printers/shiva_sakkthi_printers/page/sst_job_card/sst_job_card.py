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
      'produced_qty':int(i.produced_qty), 
      'in_process':int(i.material_transferred_for_manufacturing-i.produced_qty),
      'not_started':int(i.qty-i.material_transferred_for_manufacturing),
      'raw_material':i.required_items[0].item_name,
      'raw_material_qty':int(i.required_items[0].required_qty)  }  for i in work_order]
    status=[ i.status for i in work_order]
    workorder=[i.name for i in work_order]
    return jobcardhtml(work_order_dict,status,salesorder,workorder) if(len(work_order_dict)>0) else '<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head> <center><b> NO JOB CARDS </b></center>'
 
 
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


  
def script():
  scr= f'''
    <script>
      function start(wo){{
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
  total_papers=sum([i['raw_material_qty'] for i in wo])
  return f'''
    <div class='div'>
    Total No of Papers: {total_papers}
    </div>
  '''


def jobcardhtml(wo,status,salesorder,workorder):
  head='<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head>'
  style='''<style> 
              tr,th,td {
                border-bottom: 3px solid white;
                border-left:3px solid white;
                height:50px;
                font-size:15px;
                text-align:center;
                border-radius:10px 15px;
                border-collapse: collapse
              } 
              th{
                background-color:#ff9933;
                font-size:17px;
              }
              table{
                font-weight:bold;
              }
              button{
                border-radius:10px;
                font-weight:bold;
                padding:5px;
              }
              .jobcardinfo{
                float:left;
                width:50%;
              }
              .div{
              background-color:#33307c;
              color:white;
              font-weight:bold;
              border-radius:10px;
              height:100px;
              width:100%;
              margin-bottom:5px;
              padding:20px;
              font-size:17px;
              line-height:2;
              }
              b{
              color:black;
              font-size:17px;
              }
          </style>'''
  html='<tr>'+''.join([ f'<th>{i}</th>' for i in ['S.No','Item Name','Quantity','Stock','Produced Quantity','Production in process','Production Not Started','Paper','No of Paper','Status','Actions'] ])+'</tr>'
  color=["#ffe6ff","#FAFAD2"]
  td=[
      f'<tr style="background-color:{color[wo_details%2]};">'+f'<td>{wo_details+1}</td>'+
      ''.join([ f'<td>{wo[wo_details][list(wo[wo_details].keys())[i]]}</td>' for i in range(len(wo[wo_details])) ])+
      f'<td>{statusindicator(status[wo_details])}</td><td>{button(workorder[wo_details])}</td></tr><tr style="background-color:{color[wo_details%2]};"><td colspan=11>{progress(wo[wo_details]["produced_qty"],wo[wo_details]["in_process"],wo[wo_details]["not_started"])}</td></tr>' for wo_details in range(len(wo))]
  return head+style+script()+jobcardinfohtml(salesorder)+'<div style="width:100"><table>'+html+''.join(td)+'</table></div>'+description(wo)