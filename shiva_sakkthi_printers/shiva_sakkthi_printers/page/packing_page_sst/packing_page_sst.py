import frappe
import math

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
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":'Completed',"docstatus":1,'stock_moved':0})]
    work_order_dict=[{
      'workorder':i.item_name,
      'qty':int(i.qty),
      'stock':int(i.excess_stock),
      'production':int(i.qty)-int(i.excess_stock),
      'raw_material':i.required_items[0].item_name }  for i in work_order]
    work_order_attr=workorderfunc(work_order_dict)
    work_order_dict=work_order_sep(work_order_attr)
    
    

    if(len(work_order_dict)>0):
      html=jobcardhtml(work_order_dict,salesorder,work_order_attr)
      return html
    elif(len(frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":'Completed',"docstatus":1,'stock_moved':1}))>0):
      return '<center><b class="bold"> All Stocks are Moved </b></center>'
    elif(len([frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":['in',['In Process','Not Started']],"docstatus":1,'stock_moved':0})])>0):
      return '<center><b class="bold"> Job Cards are Not Completed </b></center>'
    else:
      return '<center><b class="bold"> No Job Cards Found </b></center>'
      
    
 
 

def work_order_sep_attr(wo, attr):
  workorder={}
  for i in wo:
    if(i[attr] in workorder):
      workorder[i[attr]].append(i)
    else:
      workorder[i[attr]]=[i]
  return workorder



def work_order_sep_attr2(wo, attr):
  workorder={}
  for i in wo:
    workorder[i]=work_order_sep_attr(wo[i],attr)
  return workorder
  


def work_order_sep_attr3(wo, attr):
  workorder={}
  for i in wo:
    if(i[attr] in workorder):
      workorder[i[attr]].append(i)
    else:
      workorder[i[attr]]=[i]
  return workorder



def work_order_sep_color(wo):
  workorder={}
  for i in wo:
    worder={}
    for j in wo[i]:
      worder[j]=work_order_sep_attr3(wo[i][j],'colour')
    workorder[i]=worder
  return workorder
  


def work_order_sep(wo):
  wo=work_order_sep_attr(wo, 'design')
  wo=work_order_sep_attr2(wo, 'raw_material')
  wo=work_order_sep_color(wo)
  return wo
  

def workorderfunc(wo):
    workorder=[]
    for i in wo:
      item=i['workorder']
      docs=frappe.get_all('Item',{'item_name':item})
      doc=frappe.get_doc('Item',docs[0].name)
      attr={}
      for j in doc.attributes:
        attr[j.attribute]=j.attribute_value
      i['size']=attr['Size']
      i['colour']=attr['Colour']
      i['design']=doc.variant_of
      workorder.append(i)
    return workorder
     
        
        
        
 

def jobcardinfohtml(salesorder,wo):
  total_qty=sum([i['qty'] for i in wo])
  so=frappe.get_doc('Sales Order',salesorder)
  infohtml=f'''
    <div class='div'>
      <div class='jobcardinfo'>
        Customer Name : {so.customer}<br>
        Delivery Date : {'-'.join(str(so.delivery_date).split('-')[::-1])}<br>
        TOTAL QUANTITY: {total_qty}<br><br>
      </div>
      <div class='jobcardinfo'>
        Job Card NO : {so.name}<br>
        PO No : {so.po_no or '-'}<br><br>
      </div>
      <div class="buttondiv">
        <button class="button" onclick="move_stock('{salesorder}')">Move Stocks</button>
      </div>
    </div>
  '''
  return infohtml



def js_script():
  script='''
  <script>
    function move_stock(so){
      frappe.call({
        method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.packing_page_sst.packing_page_sst.finish_stock_entry",
        args:{
              "so":so
             },
        callback: function(r){
          if(r.message==1){ 
            frappe.show_alert({message: __("Stocks are Moved Successfully"),indicator: 'green'});
          }
          else if(r.message==2){
            frappe.show_alert({message: __("Already Stocks are Moved!"),indicator: 'orange'});
          }
          else{
            frappe.show_alert({message: __("Can't Move Stocks"),indicator: 'red'});
          }
        }
      })
    }
  </script>
  '''
  return script
  
  
  

@frappe.whitelist()
def finish_stock_entry(so):
  try:
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':so,"status":'Completed',"docstatus":1,'stock_moved':0})]
    if(len(work_order)==0):
      return 2
    for wo_doc in work_order:
      if(wo_doc.fg_warehouse!=frappe.get_value('Sales Order',so,'set_warehouse')):
        doc=frappe.new_doc("Stock Entry")
        doc.update({
          'doctype':'Stock Entry',
          'stock_entry_type':'Material Transfer',
          'from_warehouse':wo_doc.fg_warehouse,
        })
        stock_list=[{
            "item_code" : wo_doc.production_item,
            "t_warehouse":frappe.get_value('Sales Order',so,'set_warehouse'),
            'qty':wo_doc.produced_qty
        }]
        doc.set('items', stock_list)
        doc.save()
        doc.submit()
      frappe.db.set(wo_doc, "stock_moved", 1)
      frappe.db.commit()
    return 1
  except:
    return 
  
  
  
def html_style():
  style='''
    <style>
      .designdiv{
        border: 1px solid black;
        padding: 10px;
        border-radius: 5px;
        margin-top: 15  px;
      }
      .buttondiv{
        float: right;
        position: relative;
      }
      .button{
        font-size: 17px;
        border-radius: 5px;
        font-weight: bold;
        padding: 5px;
        background-color: #4da6ff;
      }
      .table1{
        margin-bottom: 5px;
        margin-left: auto; 
        margin-right: auto;
      }
      .heading{
        font-weight: bold;
        font-size:17px;
        width:160px;
        background-color: #99ffff;
        padding: 6px;
        border: 1px solid black;
      }
      .data{
        font-size:16px;
        text-align:center;
        width:160px;
        padding: 6px;
        border: 1px solid black;
      }
      
      .jobcardinfo{
        float:left;
        width:43%;
      }
      .div{
        background-color:#003333;
        color:white;
        font-weight:bold;
        border-radius:10px;
        height:140px;
        width:100%;
        margin-bottom:5px;
        padding:20px;
        font-size:17px;
        line-height:2;
      }
      .b{
        font-size:25px;
      }
      .image{
        height: 150px;
        width: 150px;
        float: right;
        border: 1px solid black;
      }
      .nop{
        text-align: center;
        background-color:#003333;
        color:white;
        border-radius: 5px;
        padding-left: 10px;
        padding-right: 10px;
        font-weight: bold;
        font-size: 25px;
        position: absolute;
        left: 50%;
        transform: translate(-50%, 10%);
      }
    </style>
  '''
  return style


def packing_quantity(wo):
  return f'''
      <div class='nop'>
          Quantity to Pack: {sum([i["stock"]+i['production'] for i in wo])}
      </div>'''


def htmlfortable(paper,color,wo):
  workorder=[{'size':f"<b style='font-size:20px;'>{i['size']}</b>",'stock':i['stock'],
      'production':i['production'],'qty':f"<b style='font-size:21px;'>{i['qty']}</b>"} for i in wo]
  wo_list=list(zip(*[list(i.values()) for i in workorder]))
  html=f'''
    <h3>Paper : {paper}<br></h3>
    <h4>Colour : {color}<br><br><br></h4>
  '''
  trs=['<tr style="font-weight:bold;background-color: #99ffff;"><td class="heading">Size</td>',
      '<tr style="font-weight:bold;"><td class="heading">Stock</td>',
      '<tr style="font-weight:bold;"><td class="heading">Production</td>',
      '<tr style="font-weight:bold;"><td class="heading">Packing Qty</td>'] 
  table='<table class="table1">'
  for i,j in zip(trs,wo_list):
    table+=i+''.join( [f'<td class="data">{x}</td>' for x in j] )+'</tr>'
  html+=html_style()
  html+=table+'</table>' + packing_quantity(workorder)+'<BR><br><hr><br>'
  return html


def htmlforpaper(paper,wo):
  html=''
  for color in wo:
    html+=htmlfortable(paper,color,wo[color])
  return html
  

def htmlfordesign(design,wo):
  url=frappe.get_value('Item',design,'image')
  html=f'''
    <div class="designdiv">
    <img class="image" src="{url}"></img>
    <h2>Design : {design}<br></h2>
  '''
  for paper in wo:
    html+=htmlforpaper(paper,wo[paper])
  return html+'</div>'


def jobcardhtml(wo,so,unsepwo):
  htmlcode=jobcardinfohtml(so,unsepwo) + js_script()
  for design in wo:
    htmlcode+=htmlfordesign(design,wo[design])+'<br><br>  '
  return htmlcode

    
    
