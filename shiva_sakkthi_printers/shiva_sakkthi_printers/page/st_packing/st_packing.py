import frappe
from erpnext.stock.dashboard.item_dashboard import get_data

@frappe.whitelist()
def solesorderfilter(status='',customer=''):
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
      'actual_qty':int(i.qty),
      'qty':int(i.produced_qty),
      'stock':0 if(get_data(item_code=frappe.get_all("Item",{"item_name":i.item_name})[0].name , warehouse="Finished Goods - SST")==[]) else int(get_data(item_code=frappe.get_all("Item",{"item_name":i.item_name})[0].name , warehouse="Finished Goods - SST")[0]['actual_qty']) 
    }  for i in work_order]
    status=[ i.status for i in work_order]
    wo_itemcode=[frappe.get_all("Item",{'item_name':i.item_name})[0].name for i in work_order]
    wo_warehouse=[i.fg_warehouse for i in work_order]
    return jobcardhtml(wo_warehouse,wo_itemcode,work_order_dict,status,salesorder) if(len(work_order_dict)>0) else '<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head> <center><b> NO JOB CARDS </b></center>'


@frappe.whitelist()
def createstockentry(item_code,qty,warehouse):
  doc=frappe.new_doc("Stock Entry")
  doc.update({
    'doctype':'Stock Entry',
    'stock_entry_type':'Material Transfer',
    'from_warehouse':warehouse,
  })
  stock_list=[]
  stock_list.append({
      "item_code" : item_code,
      "t_warehouse":'Dispatch - SST',
      'qty':qty
  })
  stock_list.append({
      "item_code" : item_code,
      "t_warehouse":'Finished Goods - SST',
      'qty':qty
  })
  stock_list.append({
      "item_code" : item_code,
      "t_warehouse":'Damage Goods - SST',
      'qty':qty
  })
  doc.set('items', stock_list)
  doc.save()
  return doc.name



def script():
  scr= '''
    <script>
      function Completed(item_code,qty,warehouse){
        console.log(item_code);
        frappe.call(
						{
							method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.sst_packing.sst_packing.createstockentry",
							args:{
								"item_code":item_code,
                "qty":qty,
                "warehouse":warehouse
							},
							callback:function(r){
                frappe.set_route("stock-entry",r.message);
							}
            })
       
      }
    </script>
  '''
  return scr


def button(item_code,wo,warehouse):
  return f'''
    <button onclick="Completed('{item_code}','{wo['qty']}','{warehouse}')" class="Completed" type="button" style="background-color:#80ffaa; margin-bottom:4px;"> Completed </button>
  '''



def jobcardhtml(wo_warehouse,wo_itemcode,wo,status,salesorder):
  head='<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"></head>'
  style='''<style> 
              tr,th,td {
                border-bottom: 1px solid white;
                border-left:1px solid white;
                height:50px;
                font-size:15px;
                text-align:center;
                border-radius:10px 15px;
                border-collapse: collapse
              } 
              th{
                background-color:#668cff;
                font-size:17px;
              }
              table{
                font-weight:bold;
                width:100%;
              }
              button{
                border-radius:10px;
                font-weight:bold;
                padding:5px;
              }
              .jobcardinfo{
                float:left;
                width:50%;
                font-size:17px;
                line-height:2;
              }
              .div{
              background-color: #800060;
              color:white;
              font-weight:bold;
              border-radius:10px;
              height:100px;
              width:100%;
              margin-bottom:5px;
              padding:20px;
              }
          </style>'''



  html='<tr>'+''.join([ f'<th>{i}</th>' for i in ['S.No','Item Name','Actual Quantity','Produced Quantity','Packed Stock','Move'] ])+'</tr>'
  color=["#d9b3ff"," #75a3a3"]
  td=[
      f'<tr style="background-color:{color[wo_details%2]};">'+f'<td>{wo_details+1}</td>'+
      ''.join([ f'<td>{wo[wo_details][list(wo[wo_details].keys())[i]]}</td>' for i in range(len(wo[wo_details])) ])+
      f'<td>{button(wo_itemcode[wo_details],wo[wo_details],wo_warehouse[wo_details])}</td></tr>'
      for wo_details in range(len(wo))
     ]
  return head+style+script()+jobcardinfohtml(salesorder)+'<table>'+html+''.join(td)+'</table>'




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